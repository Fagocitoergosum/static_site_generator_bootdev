from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *
from pprint import pprint

md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""

print(*markdown_to_blocks(md), sep="\n")