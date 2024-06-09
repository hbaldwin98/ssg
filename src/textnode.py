from enum import Enum
from typing import override

from htmlnode import HTMLNode, LeafNode


class TextType(Enum):
    Text = ("text",)
    Bold = ("bold",)
    Italic = ("italic",)
    Code = ("code",)
    Link = ("link",)
    Image = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    @override
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TextNode):
            return False

        return (
            self.text == o.text and self.text_type == o.text_type and self.url == o.url
        )

    @override
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
