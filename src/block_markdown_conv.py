from typing import List
from enum import Enum


class BlockType(Enum):
    Paragraph = ("paragraph",)
    Header = ("header",)
    Code = ("code",)
    Quote = ("quote",)
    UnorderedList = ("unordered_list",)
    OrderedList = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if len(block) == 0:
        return BlockType.Paragraph

    if block.startswith("#"):
        space_index = block.index(" ")
        preceding_characters = block[0:space_index]
        post_characters = block[space_index:]
        if (
            len(preceding_characters) < 7
            and all(char in "#" for char in preceding_characters)
            and len(post_characters) > 0
        ):
            return BlockType.Header
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.Code
    elif block.startswith(">"):
        return BlockType.Quote
    elif block.startswith("* ") or block.startswith("- "):
        return BlockType.UnorderedList

    digits = ""
    for i in range(len(block)):
        if block[i].isdigit():
            digits += block[i]

        if digits.isdigit() and i + 2 < len(block) and block[i: i + 2] == ". ":
            return BlockType.OrderedList
        elif not block[i].isdigit():
            break

    return BlockType.Paragraph


def markdown_to_blocks(markdown: str) -> List[str]:
    return list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n")))
    )
