import os
import shutil

from block_markdown_conv import markdown_to_html_node


def search_directory(path: str) -> list[str]:
    current_dir_paths = os.listdir(path)
    files: list[str] = []

    for dir_path in current_dir_paths:
        full_path = os.path.join(path, dir_path)
        match os.path.isfile(full_path):
            case True:
                files.append(full_path)
                continue
            case False:
                files.extend(search_directory(full_path))
                continue

    return files


def copy_file_to_new_path(path: str, new_path: str):
    new_path_split = new_path.split('/')

    dir = '/'.join(new_path_split[0:-1])
    dir_exists = os.path.exists(dir)

    if not dir_exists:
        os.mkdir(dir)

    shutil.copy(path, new_path)


def clear_existing(path: str):
    if os.path.exists(path):
        shutil.rmtree(path, onexc=print(f"Removing existing path: {path}"))


def extract_title(markdown: str) -> str:
    start_header_idx = markdown.find("# ")
    if start_header_idx == -1:
        raise Exception("Markdown must have a header!")

    end_header_idx = markdown.find("\n", start_header_idx)

    if end_header_idx == -1:
        end_header_idx = len(markdown)

    return markdown[start_header_idx+2:end_header_idx].strip()


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path) as md_file:
        markdown = md_file.read()

    with open(template_path) as tp_file:
        template = tp_file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html, 1)

    destination_file_path = "/".join([dest_path, from_path.split("/")[-1].replace(".md", ".html")])
    os.makedirs(os.path.dirname(destination_file_path))
    with open(destination_file_path, "x") as dest_file:
        _ = dest_file.write(template)


def main():
    generate_page("content/index.md", "template.html", "public")


def create_public_dir():
    from_path = "static"
    dest_path = "public"

    clear_existing(dest_path)
    files = search_directory(from_path)

    for path in files:
        new_path = path.replace(from_path, dest_path, 1)
        copy_file_to_new_path(path, new_path)


if __name__ == "__main__":
    main()
