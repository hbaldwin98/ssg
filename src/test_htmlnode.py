import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_output(self):
        node = HTMLNode('This is a html node', 'bold', None, {'prop': 'value'})
        print(node)
        self.assertIsNotNone(node, 'Node is None which is not expected')

    def test_props_to_html(self):
        node = HTMLNode('This is a html node', 'bold', None,
                        {'href': 'http://test.com/'})

        self.assertEqual('href="http://test.com/"',
                         node.props_to_html(), 'Props as HTML is wrong!')


class TestLeafNode(unittest.TestCase):
    def test_output(self):
        node = LeafNode('This is a html node', 'bold', {'href': 'value'})
        print(node)
        self.assertIsNotNone(node, 'Node is None which is not expected')

    def test_to_html(self):
        node = LeafNode('p', 'This is a leaf node',
                        {'href': 'http://test.com/'})
        print(node.to_html())

        self.assertEqual('<p href="http://test.com/">This is a leaf node</p>',
                         node.to_html(), 'LeafNode as HTML is wrong!')


if __name__ == "__main__":
    unittest.main()
