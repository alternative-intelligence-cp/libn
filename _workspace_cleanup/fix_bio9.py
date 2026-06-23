import os

def fix():
    # 1. strcpy.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strcpy.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:end = dst + i;", "int64:end_ptr = dst + i;")
    content = content.replace("pass end;", "pass end_ptr;")
    with open(path, "w") as f: f.write(content)

    # 2. slab.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/slab.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("byte->", "uint8->")
    content = content.replace("<byte->>", "<uint8->>")
    content = content.replace("<byte>", "<uint8>")
    with open(path, "w") as f: f.write(content)
    
fix()
