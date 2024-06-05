import unittest

from textnode import TextNode, TextType
from main import split_nodes_delimiter


class SplitNodes(unittest.TestCase):
    def test_splits_nodes(self):
        test_cases = [
            (
                TextNode("*Test*", TextType.Text),
                "*",
                TextType.Bold,
                [TextNode("Test", TextType.Bold)],
            ),
            (
                TextNode("test *Test*", TextType.Text),
                "*",
                TextType.Bold,
                [TextNode("test ", TextType.Text),
                 TextNode("Test", TextType.Bold)],
            ),
            (
                TextNode("test *Test* test", TextType.Text),
                "*",
                TextType.Bold,
                [
                    TextNode("test ", TextType.Text),
                    TextNode("Test", TextType.Bold),
                    TextNode(" test", TextType.Text),
                ],
            ),
            (
                TextNode("This is text with a `code block` word", TextType.Text),
                "`",
                TextType.Code,
                [
                    TextNode("This is text with a ", TextType.Text),
                    TextNode("code block", TextType.Code),
                    TextNode(" word", TextType.Text),
                ],
            ),
        ]

        for case in test_cases:
            result = split_nodes_delimiter([case[0]], case[1], case[2])

            self.assertTrue(len(result) == len(case[3]))

            for i in range(len(case[3])):
                self.assertTrue(result[i].text == case[3][i].text)
                self.assertTrue(result[i].url == case[3][i].url)
                self.assertTrue(result[i].text_type == case[3][i].text_type)
