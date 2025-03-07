import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_more_children_and_nested_grandchildren(self):
        child_node_a = LeafNode("a", "Bootdev site", {"href" : "boot.dev"})
        child_node_txt = LeafNode(None, " is where I'm learning ")
        child_node_i = LeafNode("i", "this stuff")
        child_node_span = ParentNode("span", [child_node_txt, child_node_i], {"style" : "color:yellow"})
        child_node_p = ParentNode("p", [child_node_a, child_node_span])
        parent_node = ParentNode("div", [child_node_p])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><a href=\"boot.dev\">Bootdev site</a><span style=\"color:yellow\"> is where I'm learning <i>this stuff</i></span></p></div>"
        )
    
    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [LeafNode(None, "ciao")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_different_error_messages(self):
        parent_node = ParentNode(None, [LeafNode(None, "ciao")])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        no_tag_message = str(context.exception)
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        no_children_message = str(context.exception)
        self.assertNotEqual(no_tag_message, no_children_message)






if __name__ == "__main__":
    unittest.main()