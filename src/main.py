from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from html_utils import *

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

print(new_nodes)