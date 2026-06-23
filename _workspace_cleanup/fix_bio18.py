import os
import re

def fix():
    # 1. fchar.npk: fix @cast_unchecked<int64>(one) and r.is_error || r.value == 0i64
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("@cast_unchecked<int64>(one)", "@cast_unchecked<int64>(@one[0])")
    content = content.replace("if (r.is_error || r.value == 0i64) {", "if (r.is_error) { f->flags = f->flags | FILE_FLAG_EOF; pass FILE_EOF; }\n        if (r.value == 0i64) {")
    with open(path, "w") as f: f.write(content)

    # 2. strlen.npk: fix !has_nul_byte
    path = "/home/randy/Workspace/REPOS/libn/src/str/strlen.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("!has_nul_byte(", "(raw has_nul_byte(")
    content = content.replace("pw[wi]))", "pw[wi]) == false)")
    content = content.replace("int64:n = str_strnlen(s, max_len + 1i64);", "int64:n = raw str_strnlen(s, max_len + 1i64);")
    with open(path, "w") as f: f.write(content)

    # 3. fstr.npk: fix fgetc, fputs, bio_alloc_buf
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fstr.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:c = fgetc(fp);", "int64:c = raw fgetc(fp);")
    content = content.replace("int64:len = fputs(s, fp);", "int64:len = raw fputs(s, fp);")
    content = content.replace("int64:newbuf = bio_alloc_buf(new_cap);", "int64:newbuf = raw bio_alloc_buf(new_cap);")
    with open(path, "w") as f: f.write(content)

    # 4. stdfiles.npk: fix bio_alloc_buf and fputs
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("bio_alloc_buf(", "raw bio_alloc_buf(")
    content = content.replace("raw raw bio_alloc_buf", "raw bio_alloc_buf")
    content = content.replace("int64:r = fputs(s, stdout_fp);", "int64:r = raw fputs(s, stdout_fp);")
    with open(path, "w") as f: f.write(content)

fix()
