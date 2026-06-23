import os
import re

def fix():
    # 1. strerror.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("pass @cast_unchecked<int64>(g_strerror_unknown_buf);", "pass @cast_unchecked<int64>(@g_strerror_unknown_buf[0]);")
    content = content.replace("int64:msg = strerror(@cast_unchecked<int64>(libn_errno_get()));", "int64:msg = strerror(@cast_unchecked<int64>(raw libn_errno_get()));")
    content = content.replace("int64:msg = raw strerror(", "int64:msg = strerror(") # remove raw if present
    content = content.replace("int64:msg_len = raw str_strlen(msg);", "int64:msg_len = raw str_strlen(msg);")
    with open(path, "w") as f: f.write(content)

    # 2. fprintf.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
    with open(path, "r") as f: content = f.read()
    # fix missing raw on str_strlen
    content = content.replace("int64:len = str_strlen(", "int64:len = raw str_strlen(")
    content = content.replace("int64:p = mem_malloc(", "int64:p = raw mem_malloc(")
    content = content.replace("drop drop ", "drop ")
    with open(path, "w") as f: f.write(content)

fix()
