import os
import shutil


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
        shutil.rmtree(path)


def main():
    from_dir = "static"
    to_dir = "public"

    clear_existing(to_dir)
    files = search_directory(from_dir)

    for path in files:
        new_path = path.replace(from_dir, to_dir, 1)
        copy_file_to_new_path(path, new_path)


if __name__ == "__main__":
    main()
