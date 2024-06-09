import re
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


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
            return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.Text:
            new_nodes.append(node)
            continue

        split_values = node.text.split(delimiter)

        if len(split_values) % 2 == 0:
            raise ValueError("Invalid Markdown: Formatted section not closed")
        split_nodes: list[TextNode] = []

        for i in range(len(split_values)):
            if len(split_values[i]) == 0:
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(split_values[i], TextType.Text))
            else:
                split_nodes.append(TextNode(split_values[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    def split_recurse(text: str) -> list[str]:
        if text == "":
            return []

        image_tup = extract_markdown_links(text)
        if len(image_tup) == 0:
            return [text]

        result: list[str] = []
        split = text.split(f"[{image_tup[0][0]}]({image_tup[0][1]})", 1)

        if len(split) > 0 and split[0] != "":
            result.append(split[0])

        result.append(f"[{image_tup[0][0]}]({image_tup[0][1]})")

        if len(split) > 1 and split[1] != "":
            result.extend(split_recurse(split[1]))

        return result

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.Text:
            new_nodes.append(node)
            continue

        original_text = node.text

        split_values = split_recurse(original_text)
        if len(split_values) == 0:
            new_nodes.append(node)
            continue

        result: list[TextNode] = []
        for value in split_values:
            if value == "":
                continue

            image = extract_markdown_links(value)
            if len(image) > 0:
                result.append(TextNode(image[0][0], TextType.Link, image[0][1]))
            else:
                result.append(TextNode(value, TextType.Text))

        new_nodes.extend(result)

    return new_nodes


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    def split_recurse(text: str) -> list[str]:
        if text == "":
            return []

        image_tup = extract_markdown_images(text)
        if len(image_tup) == 0:
            return [text]

        result: list[str] = []
        split = text.split(f"![{image_tup[0][0]}]({image_tup[0][1]})", 1)

        if len(split) > 0 and split[0] != "":
            result.append(split[0])

        result.append(f"![{image_tup[0][0]}]({image_tup[0][1]})")

        if len(split) > 1 and split[1] != "":
            result.extend(split_recurse(split[1]))

        return result

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.Text:
            new_nodes.append(node)
            continue

        original_text = node.text

        split_values = split_recurse(original_text)
        if len(split_values) == 0:
            new_nodes.append(node)
            continue

        result: list[TextNode] = []
        for value in split_values:
            if value == "":
                continue

            image = extract_markdown_images(value)
            if len(image) > 0:
                result.append(TextNode(image[0][0], TextType.Image, image[0][1]))
            else:
                result.append(TextNode(value, TextType.Text))

        new_nodes.extend(result)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def markdown_to_nodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.Text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.Bold)
    nodes = split_nodes_delimiter(nodes, "*", TextType.Italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.Code)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes
