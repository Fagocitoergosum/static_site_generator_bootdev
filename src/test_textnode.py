import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a tes/xt node", TextType.BOLD)
        node2 = TextNode("This is a tes/xt node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("This is a tes/xt node", TextType.BOLD)
        node2 = TextNode("This is a tes/xt node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.LINK, "boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()