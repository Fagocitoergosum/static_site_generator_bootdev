from textnode import TextNode, TextType

test_node = TextNode("This is some anchor text", TextType.LINK, "www.boot.dev")

print(test_node)