import os

def fix():
    # 1. fstate.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fstate.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:newbuf = bio_alloc_buf(", "int64:newbuf = raw bio_alloc_buf(")
    with open(path, "w") as f: f.write(content)

    # 2. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("(raw ep[0]) != 0i64", "ep[0] != 0i64")
    content = content.replace("(@cast_unchecked<uint8->>(raw ep[0]))[0]", "(@cast_unchecked<uint8->>(ep[0]))[0]")
    with open(path, "w") as f: f.write(content)

    # 3. strtok.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strtok.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("&& (raw charset_test(&table[0], p[i]) == true) {", "&& (raw charset_test(&table[0], p[i]) == true)) {")
    content = content.replace("&& ((raw charset_test(&table[0], p[i]) == true) {", "&& ((raw charset_test(&table[0], p[i]) == true) == false)) {")
    with open(path, "w") as f: f.write(content)

fix()
