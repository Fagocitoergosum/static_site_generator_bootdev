import os, os.path, shutil
from md_html_utils import *

def copy_directory_tree(src, dst):
    print(f"Copying from {src} to {dst}")
    if not os.path.exists(src):
        raise Exception("Source folder not found")
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        print(f"Copying {src_path} to {dst_path}")
        if not os.path.isdir(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_directory_tree(src_path, dst_path)

def copy_static_public(static_path, public_path):
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    copy_directory_tree(static_path, public_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No title found, it must be an h1 line")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(template_path) as template_file:
        page = template_file.read()
    with open(from_path) as content_file:
        content_string = content_file.read()
    page = page.replace("{{ Title }}", extract_title(content_string)).replace("{{ Content }}", markdown_to_html_node(content_string).to_html())
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')#serve per deployare su github pages, perché il root path del sito partirà da una subdirectory
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    with open(dest_path, "w") as dest_file:
        dest_file.write(page)

def generate_pages_recursive(basepath, content_dir_path, template_path, dest_dir_path):
    #basepath la usiamo solo per sostituire la root standart negli attributi href e src nei tag html
    #per i path che usiamo per generare il sito non c'è bisogno perché la generazione avviene in locale
    for name in os.listdir(content_dir_path):
        src_path = os.path.join(content_dir_path, name)
        if os.path.isdir(src_path):
            dst_path = os.path.join(dest_dir_path, name)
            generate_pages_recursive(basepath, src_path, template_path, dst_path)
        else:
            dst_path = os.path.join(dest_dir_path, f"{name.split(".")[0]}.html")
            generate_page(basepath, src_path, template_path, dst_path)