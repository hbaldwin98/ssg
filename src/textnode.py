from enum import Enum
from typing import override


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
