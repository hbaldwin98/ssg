import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_when_children_is_none(self):
        node = ParentNode("p", None, {"prop": "value"})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_single_child(self):
        child_node = LeafNode("strong", "this is some text", None)
        node = ParentNode("p", [child_node], {"style": "margin: 1rem"})

        self.assertEqual(
            node.to_html(),
            '<p style="margin: 1rem"><strong>this is some text</strong></p>',
        )

    def test_to_html_with_two_children(self):
        child_node = LeafNode("strong", "this is some text", None)
        child_node_2 = LeafNode(
            "p", "this is some text as well", {"color": "red"})
        node = ParentNode("p", [child_node, child_node_2], {
                          "style": "margin: 1rem"})

        self.assertEqual(
            node.to_html(),
            '<p style="margin: 1rem"><strong>this is some text</strong><p color="red">this is some text as well</p></p>',
        )

    def test_to_html_with_nested_parent(self):
        child_node = LeafNode("strong", "this is some text", None)
        child_node_2 = LeafNode(
            "span", "this is some text as well", {"color": "red"})
        nested_parent_node = ParentNode("p", [child_node_2], None)
        node = ParentNode(
            "p", [child_node, nested_parent_node], {"style": "margin: 1rem"}
        )

        self.assertEqual(
            node.to_html(),
            '<p style="margin: 1rem"><strong>this is some text</strong><p><span color="red">this is some text as well</span></p></p>',
        )
