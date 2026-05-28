import unittest
from textnode import TextNode, TextType
from text_parsing import split_nodes_delimiter


class TestTextParsing(unittest.TestCase):
    def test_split_nodes_delimiter_text_to_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_non_text_nodes_unchanged(self):
        node = TextNode("No split", TextType.CODE)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_unbalanced_delimiter_raises(self):
        node = TextNode("Missing end `code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
