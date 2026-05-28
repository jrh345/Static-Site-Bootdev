import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag(self):
        node = LeafNode("h1", "Hello")
        self.assertEqual(node.to_html(), "<h1>Hello</h1>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Link", {"href": "http://example.com", "class": "btn"})
        self.assertEqual(node.to_html(), '<a href="http://example.com" class="btn">Link</a>')

    def test_to_html_without_tag(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_value_none_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_empty_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", "").to_html()

    def test_eq(self):
        n1 = LeafNode("span", "x", {"a": "1"})
        n2 = LeafNode("span", "x", {"a": "1"})
        n3 = LeafNode("span", "y", {"a": "1"})
        self.assertEqual(n1, n2)
        self.assertNotEqual(n1, n3)


if __name__ == "__main__":
    unittest.main()
