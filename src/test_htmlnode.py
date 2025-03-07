import unittest
from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("a", "diocan", None, {"href": "https://www.google.com",
                                            "target": "_blank"}
                        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty_dict(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_to_html_raises_not_implemented_error(self):
        node = HtmlNode(tag="p", value="test")
        # Test that calling `to_html` raises a NotImplementedError
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Bootdev site", {"href" : "boot.dev"})
        self.assertEqual(node.to_html(), '<a href="boot.dev">Bootdev site</a>')
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()




if __name__ == "__main__":
    unittest.main()