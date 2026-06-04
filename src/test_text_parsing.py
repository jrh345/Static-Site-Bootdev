import unittest
from textnode import TextNode, TextType
from text_parsing import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, 
                         split_nodes_image, split_nodes_link, text_to_textnodes)


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a link [to boot dev](https://www.boot.dev)" +
                " and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(matches, [("to boot dev", "https://www.boot.dev"), 
                              ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)" + 
        " and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_non_text_node_unchanged(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.CODE)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) trailing text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_image_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            split_nodes_image([node]),
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)" + 
            " and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_non_text_node_unchanged(self):
        node = TextNode("[link](https://www.boot.dev)", TextType.CODE)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_link_at_start(self):
        node = TextNode("[to boot dev](https://www.boot.dev) trailing text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_link_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")],
            split_nodes_link([node]),
        )

    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word and a `code block`" 
                " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        text_to_textnodes(text)
                             )
    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text"
        self.assertListEqual(
            [TextNode("This is plain text", TextType.TEXT)],
            text_to_textnodes(text)
            )

    def test_text_to_textnodes_bold_only(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**")
        )

    def test_text_to_textnodes_italic_only(self):
        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            text_to_textnodes("_italic_")
        )

    def test_text_to_textnodes_code_only(self):
        self.assertListEqual(
            [TextNode("code", TextType.CODE)],
            text_to_textnodes("`code`")
        )

    def test_text_to_textnodes_image_only(self):
        self.assertListEqual(
            [TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")],
            text_to_textnodes("![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        )

    def test_text_to_textnodes_link_only(self):
        self.assertListEqual(
            [TextNode("boot dev", TextType.LINK, "https://boot.dev")],
            text_to_textnodes("[boot dev](https://boot.dev)")
        )

    def test_text_to_textnodes_unbalanced_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unbalanced")

if __name__ == "__main__":
    unittest.main()
