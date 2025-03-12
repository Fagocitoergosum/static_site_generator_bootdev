from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *

node = TextNode(
    #"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    "This is a text ebbasta",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])

print(new_nodes)