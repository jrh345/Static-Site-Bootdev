import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})
        node2 = HTMLNode("h1", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})
        node3 = HTMLNode("h1", "value string",[HTMLNode("child 2")],{"href":"https://www.google.com"})
        node4 = HTMLNode("p", "value string",[HTMLNode("child 1")],{"href":"https://www.google.com"})

        self.assertEqual(node, node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node,node4)

if __name__ == "__main__":
    unittest.main()
