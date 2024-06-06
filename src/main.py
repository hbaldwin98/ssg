from textnode import TextNode, TextType
from inline_markdown_conv import text_node_to_html_node


def main():
    node = TextNode("This is a test", TextType.Link, "test.com")
    print(text_node_to_html_node(node))
    node = TextNode("This is a test", TextType.Text, None)
    print(text_node_to_html_node(node))


if __name__ == "__main__":
    main()
