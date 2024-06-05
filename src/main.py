from typing import List, Tuple
import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.Text:
            return LeafNode(None, text_node.text)
        case TextType.Bold:
            return LeafNode("strong", text_node.text)
        case TextType.Italic:
            return LeafNode("em", text_node.text)
        case TextType.Code:
            return LeafNode("code", text_node.text)
        case TextType.Link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.Image:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text_node type supplied.")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[HTMLNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.Text:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            raise Exception(
                f"ERROR! Node with text: {node.text}\nInvalid markdown syntax."
            )

        split_values = node.text.split(delimiter)

        if len(split_values) % 2 == 0:
            raise ValueError("Invalid Markdown: Formatted section not closed")
        split_nodes = []

        for i in range(len(split_values)):
            if len(split_values[i]) == 0:
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(split_values[i], TextType.Text))
            else:
                split_nodes.append(TextNode(split_values[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> Tuple[str, str]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> Tuple[str, str]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def main():
    node = TextNode("This is a test", TextType.Link, "test.com")
    print(text_node_to_html_node(node))
    node = TextNode("This is a test", TextType.Text, None)
    print(text_node_to_html_node(node))


if __name__ == "__main__":
    main()
