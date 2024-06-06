from inline_markdown_conv import (
    extract_markdown_images,
    split_nodes_images,
    split_nodes_links,
    split_nodes_delimiter,
)
import unittest

from textnode import TextNode, TextType


class InlineMarkdownTests(unittest.TestCase):
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

    def MarkdownConversionTests(self):
        test_cases = [
            (
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                (
                    [
                        (
                            "image",
                            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                        ),
                        (
                            "another",
                            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                        ),
                    ]
                ),
            )
        ]

        for test_case in test_cases:
            output = extract_markdown_images(test_case[0])
            for i in range(len(output)):
                self.assertTrue(output[i][0] == test_case[1][i][0])
                self.assertTrue(output[i][1] == test_case[1][i][1])

    def test_extract_links(self):
        test_cases = [
            (
                "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                (
                    [
                        (
                            "link",
                            "https://www.example.com",
                        ),
                        (
                            "another",
                            "https://www.example.com/another",
                        ),
                    ]
                ),
            )
        ]

        for test_case in test_cases:
            output = extract_markdown_images(test_case[0])
            for i in range(len(output)):
                self.assertTrue(output[i][0] == test_case[1][i][0])
                self.assertTrue(output[i][1] == test_case[1][i][1])

    def test_split_images(self):
        test_cases = [
            (
                TextNode(
                    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                    TextType.Text,
                ),
                [
                    TextNode("This is text with an ", TextType.Text),
                    TextNode(
                        "image",
                        TextType.Image,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                    ),
                    TextNode(" and ", TextType.Text),
                    TextNode(
                        "another",
                        TextType.Image,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                    ),
                ],
            ),
            (
                TextNode("No image here folks", TextType.Text),
                [TextNode("No image here folks", TextType.Text)],
            ),
            (
                TextNode("![image](https://example.com/)", TextType.Text),
                [TextNode("image", TextType.Image, "https://example.com/")],
            ),
            (
                TextNode(
                    "![image](https://example.com/) ![another one](https://example.com/)",
                    TextType.Text,
                ),
                [
                    TextNode("image", TextType.Image, "https://example.com/"),
                    TextNode(" ", TextType.Text),
                    TextNode("another one", TextType.Image,
                             "https://example.com/"),
                ],
            ),
            (
                TextNode("[link][https://noimageherefolks.com/]",
                         TextType.Text),
                [TextNode("[link][https://noimageherefolks.com/]", TextType.Text)],
            ),
        ]

        for test_case in test_cases:
            result = split_nodes_images([test_case[0]])
            for i in range(len(test_case[1])):
                self.assertTrue(
                    test_case[1][i].text == result[i].text,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )
                self.assertTrue(
                    test_case[1][i].text_type == result[i].text_type,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )
                self.assertTrue(
                    test_case[1][i].url == result[i].url,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )

    def test_split_links(self):
        test_cases = [
            (
                TextNode(
                    "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                    TextType.Text,
                ),
                [
                    TextNode("This is text with an ", TextType.Text),
                    TextNode(
                        "link",
                        TextType.Link,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                    ),
                    TextNode(" and ", TextType.Text),
                    TextNode(
                        "another",
                        TextType.Link,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                    ),
                ],
            ),
            (
                TextNode("No link here folks", TextType.Text),
                [TextNode("No link here folks", TextType.Text)],
            ),
            (
                TextNode("[image](https://example.com/)", TextType.Text),
                [TextNode("image", TextType.Link, "https://example.com/")],
            ),
            (
                TextNode(
                    "[image](https://example.com/) [another one](https://example.com/)",
                    TextType.Text,
                ),
                [
                    TextNode("image", TextType.Link, "https://example.com/"),
                    TextNode(" ", TextType.Text),
                    TextNode("another one", TextType.Link,
                             "https://example.com/"),
                ],
            ),
            (
                TextNode(
                    "![image](https://example.com/) [another one](https://example.com/)",
                    TextType.Text,
                ),
                [
                    TextNode("![image](https://example.com/) ", TextType.Text),
                    TextNode("another one", TextType.Link,
                             "https://example.com/"),
                ],
            ),
        ]

        for test_case in test_cases:
            result = split_nodes_links([test_case[0]])
            for i in range(len(test_case[1])):
                self.assertTrue(
                    test_case[1][i].text == result[i].text,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )
                self.assertTrue(
                    test_case[1][i].text_type == result[i].text_type,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )
                self.assertTrue(
                    test_case[1][i].url == result[i].url,
                    f"Result: {result[i]}, Expected: {test_case[1][i]}",
                )
