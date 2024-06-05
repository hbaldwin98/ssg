import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_output(self):
        node = HTMLNode("This is a html node", "bold", None, {"prop": "value"})
        self.assertIsNotNone(node, "Node is None which is not expected")

    def test_props_to_html(self):
        node = HTMLNode(
            "This is a html node", "bold", None, {"href": "http://test.com/"}
        )

        self.assertEqual(
            'href="http://test.com/"', node.props_to_html(), "Props as HTML is wrong!"
        )


class TestLeafNode(unittest.TestCase):
    def test_output(self):
        node = LeafNode("This is a html node", "bold", {"href": "value"})
        self.assertIsNotNone(node, "Node is None which is not expected")

    def test_to_html(self):
        node = LeafNode("p", "This is a leaf node", {
                        "href": "http://test.com/"})
        self.assertEqual(
            '<p href="http://test.com/">This is a leaf node</p>',
            node.to_html(),
            "LeafNode as HTML is wrong!",
        )

    def test_without_tag_only_value(self):
        node = LeafNode(
            None, "This is a leaf node without a tag or props", None)

        self.assertEqual(
            'This is a leaf node without a tag or props',
            node.to_html(),
            "LeafNode as HTML is wrong! Shouldn't have tags or props!'",
        )


if __name__ == "__main__":
    unittest.main()
