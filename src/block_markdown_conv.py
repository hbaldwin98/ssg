from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown_conv import markdown_to_nodes, text_node_to_html_node
from textnode import TextNode


class BlockType(Enum):
    Paragraph = ("paragraph",)
    Header = ("header",)
    Code = ("code",)
    Quote = ("quote",)
    UnorderedList = ("unordered_list",)
    OrderedList = "ordered_list"


def block_to_block_type(markdown: str) -> BlockType:
    if markdown.startswith("#"):
        space_index = markdown.index(" ")
        preceding_characters = markdown[0:space_index]
        post_characters = markdown[space_index:]
        if (
            len(preceding_characters) < 7
            and all(char in "#" for char in preceding_characters)
            and len(post_characters) > 0
        ):
            return BlockType.Header

    lines = markdown.split("\n")

    if len(lines) == 0:
        return BlockType.Paragraph

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.Code

    if markdown.startswith(">"):
        if not all_start_with(lines, ">"):
            return BlockType.Paragraph

        return BlockType.Quote

    if markdown.startswith("* "):
        if not all_start_with(lines, "* "):
            return BlockType.Paragraph

        return BlockType.UnorderedList

    if markdown.startswith("- "):
        if not all_start_with(lines, "- "):
            return BlockType.Paragraph

        return BlockType.UnorderedList

    if markdown.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.Paragraph

        return BlockType.OrderedList

    return BlockType.Paragraph


def all_start_with(list: list[str], match: str) -> bool:
    return all(map(lambda x: x.startswith(match), list))


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(
        filter(lambda x: x != "", map(
            lambda x: x.strip(), markdown.split("\n\n")))
    )


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes: list[HTMLNode] = []
    for block in blocks:
        child_blocks: list[HTMLNode] | None = []
        block_type = block_to_block_type(block)
        tag = ""

        match block_type:
            case BlockType.Paragraph:
                tag = "p"
            case BlockType.Code:
                tag = "pre"
            case BlockType.OrderedList:
                tag = "ol"
            case BlockType.UnorderedList:
                tag = "ul"
            case BlockType.Quote:
                tag = "blockquote"
            case BlockType.Header:
                split_block = block.split(' ')
                number_hashes = len(split_block[0])
                tag = f"h{number_hashes}"

        is_list_block = block_type in [BlockType.OrderedList, BlockType.UnorderedList]

        lines = block.split('\n')
        for line in lines:
            if is_list_block:
                child_blocks.append(ParentNode("li", text_to_children(line[2:].strip())))

        if is_list_block:
            block = None
        elif block_type is BlockType.Code:
            child_blocks.append(ParentNode('code', text_to_children(block)))
            block = None
        elif block_type is not BlockType.Paragraph:
            block = block.split(' ', 1)[1]

        if len(child_blocks) == 0:
            child_blocks = None

            nodes.append(ParentNode(tag, text_to_children(block)))
        else:
            nodes.append(ParentNode(tag, child_blocks))

    return ParentNode("div", nodes)


def text_to_children(text: str | None) -> list[HTMLNode]:
    if text is None:
        return []

    text_nodes: list[TextNode] = markdown_to_nodes(text)
    children: list[HTMLNode] = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children
