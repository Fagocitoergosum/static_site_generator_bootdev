from textnode import TextNode, TextType
from htmlnode import HtmlNode

test_node = HtmlNode("a", "diocan", [HtmlNode()], {"href": "https://www.google.com",
                                            "target": "_blank"}
                    )

print(test_node)