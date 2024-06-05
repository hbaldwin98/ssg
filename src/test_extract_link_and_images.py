import unittest
from main import extract_markdown_images, extract_markdown_links


class ExtractLinksAndImages(unittest.TestCase):
    def test_extract_images(self):
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
