from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise Exception("text node has invalid text_type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:                
            new_nodes_texts = node.text.split(delimiter)
            if len(new_nodes_texts) %2 == 0:
                raise Exception("Number of delimiters in string not matching. This is invalid Markdown syntax")
            new_node_text_type = TextType.TEXT
            for new_text in new_nodes_texts:
                if new_text != "":
                    new_nodes.append(TextNode(new_text, new_node_text_type))
                    if new_node_text_type == TextType.TEXT:
                        new_node_text_type = text_type
                    else:
                        new_node_text_type = TextType.TEXT
        else:
            new_nodes.append(node)
    return new_nodes