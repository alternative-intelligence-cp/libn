import os

def fix():
    # 1. fchar.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("@one[0]", "@one")
    with open(path, "w") as f: f.write(content)

    # 2. strfmt.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strfmt.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("@nbuf[0]", "@nbuf")
    with open(path, "w") as f: f.write(content)

fix()
