import unittest

from htmlnode import HTMLNode
from block_markdown_conv import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType,
)


class BlockMarkdownConversionTests(unittest.TestCase):
    def test_properly_splits_on_block(self):
        input = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\n"
            "This is the same paragraph on a new line",
            "* This is a list\n" "* with items",
        ]

        self.assertListEqual(
            markdown_to_blocks(input), expected, "Split blocks not as expected"
        )

    def test_properly_determines_block_type(self):
        test_cases = [
            ("* This is a list item", BlockType.UnorderedList),
            ("- This is a list item", BlockType.UnorderedList),
            ("1. This is an ordered list item", BlockType.OrderedList),
            (
                "1. This is an ordered list item\n"
                "2. And this is the seoncd line for the list item",
                BlockType.OrderedList,
            ),
            (
                "100. This is also an ordered list item but out of order",
                BlockType.Paragraph,
            ),
            ("> This is a quote", BlockType.Quote),
            ("> This is a quote\nthat fails in being a quote", BlockType.Paragraph),
            ("# This is a level 1 header", BlockType.Header),
            ("## This is a level 2 header", BlockType.Header),
            ("### This is a level 3 header", BlockType.Header),
            ("#### This is a level 4 header", BlockType.Header),
            ("##### This is a level 5 header", BlockType.Header),
            ("###### This is a level 6 header", BlockType.Header),
            ("```This is a code quote```", BlockType.Code),
            ("```This is a code quote\nand it continues here```", BlockType.Code),
            ("```This is a code quote\nwithout an ending", BlockType.Paragraph),
            ("This is a paragraph", BlockType.Paragraph),
        ]

        for test_case in test_cases:
            result = block_to_block_type(test_case[0])
            self.assertEqual(
                test_case[1],
                result,
                f"\nResult is unexpected. \n\nExpected: {
                    test_case[1]}\nActual: {result}",
            )

    def test_markdown_to_html_node(self):
        test_cases = [
            (
                "* This is a list item",
                [HTMLNode("ul", None, [HTMLNode("li", "This is a list item")])],
            ),
            (
                "* This is a list item\n* This is another list item",
                [
                    HTMLNode(
                        "ul",
                        None,
                        [
                            HTMLNode("li", "This is a list item"),
                            HTMLNode("li", "This is another list item"),
                        ],
                    )
                ],
            ),
            (
                "1. This is a list item\n2. This is another list item",
                [
                    HTMLNode(
                        "ol",
                        None,
                        [
                            HTMLNode("li", "This is a list item"),
                            HTMLNode("li", "This is another list item"),
                        ],
                    )
                ],
            ),
            (
                "## This is a header item",
                [
                    HTMLNode(
                        "h2",
                        "This is a header item",
                    )
                ],
            ),
            (
                "This is a paragraph item",
                [
                    HTMLNode(
                        "p",
                        "This is a paragraph item",
                    )
                ],
            ),
            (
                "```This is a code item```",
                [HTMLNode("pre", None, [HTMLNode("code", "This is a code item")])],
            ),
            (
                """# Header 1

## Header 2

This is a paragraph.

1. Ordered list item 1
2. Ordered list item 2

- Unordered list item 1
- Unordered list item 2

> BlockQuote""",
                [
                    HTMLNode("h1", "Header 1"),
                    HTMLNode("h2", "Header 2"),
                    HTMLNode("p", "This is a paragraph."),
                    HTMLNode(
                        "ol",
                        None,
                        [
                            HTMLNode("li", "Ordered list item 1"),
                            HTMLNode("li", "Ordered list item 2"),
                        ],
                    ),
                    HTMLNode(
                        "ul",
                        None,
                        [
                            HTMLNode("li", "Unordered list item 1"),
                            HTMLNode("li", "Unordered list item 2"),
                        ],
                    ),
                    HTMLNode(
                        "blockquote",
                        "BlockQuote",
                    ),
                ],
            ),
        ]

        def assert_values(result, expected):
            self.assertTrue(
                result.tag == expected.tag,
                f"Tag is wrong\n\nExpected: {
                    expected.value}\nActual: {result.value}",
            )
            self.assertTrue(
                result.value == expected.value,
                f"Value is wrong\n\nExpected: {
                    expected.value}\nActual: {result.value}",
            )

            if result.children is not None:
                for i in range(len(result.children)):
                    assert_values(result.children[i], expected.children[i])

        for test_case in test_cases:
            result: list[HTMLNode] = markdown_to_html_node(
                test_case[0]).children
            for i in range(len(result)):
                assert_values(result[i], test_case[1][i])
