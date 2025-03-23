from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *
from page_generation_utils import *
from pprint import pprint
'''
md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""

blocks = markdown_to_blocks(md)
#print(*blocks, sep="\n")

print(block_to_block_type(blocks[2]))
'''
#print(os.listdir("."))
copy_static_public("static", "public")
generate_page("content/index.md", "template.html", "public/index.html")