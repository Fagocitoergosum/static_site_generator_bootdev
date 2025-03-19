from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

def extract_markdown_images(text):
    #[^ ] matcha i caratteri che non sono nel set definito all'interno di [] 
    #quindi in questo caso matcha tutti i caratteri che non sono parentesi quadre nel primo e tonde nel secondo capturing group
    #in questo modo se abbiamo una parentesi mismatched tipo ![alt t[ext](url.)of.image) è una sintassi markdown non valida e non la matcha
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text != '':
                tmp_text = node.text
                url_tuples = extract_markdown_images(node.text)
                for url_tuple in url_tuples:
                    new_texts = tmp_text.split(f"![{url_tuple[0]}]({url_tuple[1]})", 1)
                    if new_texts[0] != '':
                        new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
                    new_nodes.append(TextNode(url_tuple[0], TextType.IMAGE, url_tuple[1]))
                    tmp_text = new_texts[1]
                if tmp_text != '':
                    new_nodes.append(TextNode(tmp_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text != '':
                tmp_text = node.text
                url_tuples = extract_markdown_links(node.text)
                for url_tuple in url_tuples:
                    new_texts = tmp_text.split(f"[{url_tuple[0]}]({url_tuple[1]})", 1)
                    if new_texts[0] != '':
                        new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
                    new_nodes.append(TextNode(url_tuple[0], TextType.LINK, url_tuple[1]))
                    tmp_text = new_texts[1]
                if tmp_text != '':
                    new_nodes.append(TextNode(tmp_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

#anche se si chiama text_to_textnodes il parametro text è una lista con un unico textnode con text_type TEXT
def text_to_textnodes(text):
    nodes = split_nodes_delimiter(text, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda md: md!="", map(
                lambda md: md.strip("\n \t"), 
                markdown.split("\n\n")
                )
            )
        )

def block_to_block_type(block):
    heading_regex = re.compile(r"#{1,6} .*?", re.DOTALL)
    if heading_regex.match(block):
        return BlockType.HEADING
    code_regex = re.compile(r"^```.*```\Z", re.DOTALL)#matcha inizio stringa, tutto ciò che è racchiuso tra i ``` e fine stringa
    if code_regex.match(block):
        return BlockType.CODE
    quote_regex = re.compile(r"(?:^>.*)+\Z", re.MULTILINE|re.DOTALL)#(?:...) è un non capturing group, matcha ciò che c'è tra le parentesi ma non permette di acedervi
    if quote_regex.match(block):
        return BlockType.QUOTE
    unordered_list_regex = re.compile(r"^- .*")
    if all(map(lambda str: unordered_list_regex.match(str) ,block.split("\n"))):
        return BlockType.UNORDERED_LIST
    ordered_list_regex = re.compile(r"^\d\. .*")
    if all(map(lambda str: ordered_list_regex.match(str) ,block.split("\n"))):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def count_heading_number(heading_block):
    count = 0
    i = 0
    while heading_block[i] == "#":
        count += 1
        i += 1
    return count

def text_to_children(text):
    text_nodes = text_to_textnodes([TextNode(text.replace("\n"," "), TextType.TEXT)])
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes

def markdown_to_html_node(markdown):
    print(f"MD:\n{markdown}")
    blocks = markdown_to_blocks(markdown)
    print(f"Blocks:\n{blocks}")
    parent_div = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                new_node = ParentNode(f"h{count_heading_number(block)}", text_to_children(block.lstrip("# ")))
            case BlockType.CODE:
                new_node = ParentNode("pre", [text_node_to_html_node(TextNode(block.strip("`\n"),TextType.CODE))])
            case BlockType.QUOTE:
                lines = " ".join(map(lambda line: line.lstrip(">"), block.split("\n")))
                new_node = ParentNode("blockquote", text_to_children(lines))
            case BlockType.UNORDERED_LIST:
                lines = list(map(lambda line: line.lstrip("- "), block.split("\n")))
                new_node = ParentNode("ul", list(map(lambda line: ParentNode("li", text_to_children(line)), lines)))
            case BlockType.ORDERED_LIST:
                lines = list(map(lambda line: line.lstrip("0123456789. "), block.split("\n")))
                new_node = ParentNode("ol", list(map(lambda line: ParentNode("li", text_to_children(line)), lines)))
            case BlockType.PARAGRAPH:
                new_node = ParentNode("p", text_to_children(block))
        parent_div.children.append(new_node)
    return parent_div