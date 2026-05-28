import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})
        node2 = HTMLNode("h1", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})
        node3 = HTMLNode("h1", "value string",[HTMLNode("child 2")],{"href":"https://www.google.com"})
        node4 = HTMLNode("p", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})

        self.assertEqual(node, node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node,node4)

    def test_props_to_html_with_props(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty_or_none(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), '')
        node2 = HTMLNode("p", "text", props={})
        self.assertEqual(node2.props_to_html(), '')

    def test_repr_contains_fields(self):
        node = HTMLNode("div", "x", [HTMLNode("child")], {"id": "1"})
        r = repr(node)
        self.assertIn("HTMLNode", r)
        self.assertIn("div", r)
        self.assertIn("x", r)
        self.assertIn("id", r)

    def test_parentnode_to_html_recursive(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_with_props(self):
        node = ParentNode("div", [LeafNode(None, "x")], {"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test">x</div>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "one"),
                LeafNode("span", "two"),
                LeafNode("span", "three"),
            ],
        )
        self.assertEqual(node.to_html(), "<div><span>one</span><span>two</span><span>three</span></div>")

    def test_parentnode_missing_tag_raises(self):
        node = ParentNode(None, [LeafNode(None, "x")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_missing_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
