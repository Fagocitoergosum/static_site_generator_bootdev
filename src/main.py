from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *

node = TextNode(
    #"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
    TextType.TEXT,
)
new_nodes = text_to_textnodes([node])

print(*new_nodes, sep="\n")