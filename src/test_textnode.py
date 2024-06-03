import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', 'bold', 'test.url')
        node2 = TextNode('This is a text node', 'bold', 'test.url')
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
