import unittest

from block_markdown_conv import markdown_to_blocks, block_to_block_type, BlockType


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
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            "* This is a list",
            "* with items",
        ]

        self.assertListEqual(
            markdown_to_blocks(input), expected, "Split blocks not as expected"
        )

    def test_properly_determines_block_type(self):
        test_cases = [
            ("* This is a list item", BlockType.UnorderedList),
            ("- This is a list item", BlockType.UnorderedList),
            ("1. This is an ordered list item", BlockType.OrderedList),
            ("100. This is also an ordered list item", BlockType.OrderedList),
            ("> This is a quote", BlockType.Quote),
            ("# This is a level 1 header", BlockType.Header),
            ("## This is a level 2 header", BlockType.Header),
            ("### This is a level 3 header", BlockType.Header),
            ("#### This is a level 4 header", BlockType.Header),
            ("##### This is a level 5 header", BlockType.Header),
            ("###### This is a level 6 header", BlockType.Header),
            ("```This is a code quote```", BlockType.Code),
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
