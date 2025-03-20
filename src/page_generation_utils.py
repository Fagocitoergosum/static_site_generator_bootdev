import os, os.path, shutil

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