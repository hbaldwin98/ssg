import unittest
from main import extract_title


class TestGeneration(unittest.TestCase):
    def test_extract_title(self):
        test_cases = [
            ("# This is a title", "This is a title"),
            ("# This is a title\nwith a new line", "This is a title"),
            ("This does not have a title", ""),
            ("This has a title\n# On the second line!", None),
            ("", None),
            ("#Thisisbroken", None),
        ]

        for test_case in test_cases:
            try:
                result = extract_title(test_case[0])
                self.assertTrue(result == test_case[1], f"Invalid result!\n\nExpected: {
                    test_case[1]}\nActual:{result}")
            except Exception as e:
                self.assertTrue(e, "Markdown must have a header!")
