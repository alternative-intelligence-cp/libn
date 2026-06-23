import os

def fix():
    # 1. strbuf.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strbuf.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:n = str_strlen(", "int64:n = raw str_strlen(")
    with open(path, "w") as f: f.write(content)

    # 2. strchr.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strchr.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("true) {", "true)) {")
    content = content.replace("false) {", "false)) {")
    with open(path, "w") as f: f.write(content)

    # 3. stdfiles.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("(@cast_unchecked<uint8->>(ep[0]))[0]", "(@cast_unchecked<uint8->>(raw ep[0]))[0]")
    content = content.replace("ep[0] != 0i64", "(raw ep[0]) != 0i64")
    with open(path, "w") as f: f.write(content)

fix()
