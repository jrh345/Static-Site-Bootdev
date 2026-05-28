from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text] (url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        if (self.text == other.text and self.text_type == other.text_type and self.url == other.url):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match (text_node.text_type):
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")