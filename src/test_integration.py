import unittest
from textnode import TextType, TextNode
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *

class TestNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")
    
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertDictEqual(html_node.props, {"href" : "boot.dev"})
        self.assertEqual(html_node.to_html(), "<a href=\"boot.dev\">This is a link node</a>")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src" : "url/of/image.jpg", "alt" : "This is an image node"})
        self.assertEqual(html_node.to_html(), "<img src=\"url/of/image.jpg\" alt=\"This is an image node\"></img>")

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD),TextNode(" word", TextType.TEXT),])

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC),TextNode(" word", TextType.TEXT),])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT),])

    def test_multiword_section(self):
        node = TextNode("This is text with a **bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold word", TextType.BOLD)])

    def test_multiple_sections_same_delimiter(self):
        node = TextNode("This is text with _more_ italic _words_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with ", TextType.TEXT), TextNode("more", TextType.ITALIC),TextNode(" italic ", TextType.TEXT),TextNode("words", TextType.ITALIC)])

    def test_multiple_sections_different_delimiters(self):
        node = TextNode("This is text with an _italic_ and a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC),TextNode(" and a ", TextType.TEXT),TextNode("bold",TextType.BOLD), TextNode(" word",TextType.TEXT)])

    def test_no_matching_delimiters(self):
        node = TextNode("This is song with no words, nobody can sing or miss it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is song with no words, nobody can sing or miss it", TextType.TEXT)])

    def test_mismatched_delimiter(self):
        node = TextNode("This_ is text with an _italic_ word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_markdown_images(text),[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images_mismatched_parentheses(self):
        matches = extract_markdown_images("This is text with an ![imag[e](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(matches, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_extract_markdown_links_mismatched_parentheses(self):
        text = "This is text with a link [to bo]ot dev](https://www.boot.dev)"
        self.assertListEqual(extract_markdown_links(text), [])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
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
    
    def test_split_images_ending_with_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) which ends with text",
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
                TextNode(" which ends with text", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_images_starting_with_image(self):
        node = TextNode(
            "![This is an image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is a text with no images", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [TextNode("This is a text with no images",TextType.TEXT)])
    
    def test_split_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [])

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_ending_with_text(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://google.com) ending with text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com"
                ),
                TextNode(" ending with text", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links_starting_with_link(self):
        node = TextNode(
            "[This is a link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com"
                ),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is a text with no links", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [TextNode("This is a text with no links",TextType.TEXT)])
    
    def test_split_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [])
    
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT
        )
        expected_result = [
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
        ]
        self.assertListEqual(text_to_textnodes([node]), expected_result)
    
    def test_text_to_textnodes_text_only(self):
        node = TextNode("This is only text", TextType.TEXT)
        expected_result = [TextNode("This is only text", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes([node]), expected_result)
    
    def test_text_to_textnodes_link_only(self):
        node = TextNode("[Just a link](https://boot.dev)", TextType.TEXT)
        expected_result = [TextNode("Just a link", TextType.LINK, "https://boot.dev")]
        self.assertListEqual(text_to_textnodes([node]), expected_result)
    
    def test_text_to_textnodes_image_only(self):
        node = TextNode("![Just an image](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        expected_result = [TextNode("Just an image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(text_to_textnodes([node]), expected_result)

    def test_text_to_textnodes_no_nodes(self):
        self.assertListEqual(text_to_textnodes([]), [])

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_strip(self):
        md = """
        This is **bolded** paragraph

       This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), [])




if __name__ == "__main__":
    unittest.main()