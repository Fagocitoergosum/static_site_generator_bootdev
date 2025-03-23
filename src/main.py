from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from md_html_utils import *
from page_generation_utils import *
from pprint import pprint
import sys

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

#sostituiamo docs a public perché la directory di default dalla quale github servirà il sito è la directory docs del branch main
#copy_static_public("static", "public")
#generate_pages_recursive(basepath, "content", "template.html", "public")

copy_static_public("static", "docs")
generate_pages_recursive(basepath, "content", "template.html", "docs")