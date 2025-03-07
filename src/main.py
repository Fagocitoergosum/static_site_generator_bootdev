from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode

child_node_a = LeafNode("a", "Bootdev site", {"href" : "boot.dev"})
child_node_txt = LeafNode(None, " is where I'm learning ")
child_node_i = LeafNode("i", "this stuff")
child_node_span = ParentNode("span", [child_node_txt, child_node_i], {"style" : "color:yellow"})
child_node_p = ParentNode("p", [child_node_a, child_node_span])
test_node = ParentNode("div", [child_node_p])

print(test_node.to_html())