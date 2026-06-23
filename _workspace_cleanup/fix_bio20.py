import os
import re

def fix():
    # 1. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64->:ep = @cast_unchecked<int64->>(endptr_val);", "int64->:ep = @cast_unchecked<int64->>(@endptr_val[0]);")
    content = content.replace("errno_get()", "libn_errno_get()")
    content = content.replace("errno_clear()", "libn_errno_set(0i64)")
    with open(path, "w") as f: f.write(content)

    # 2. stdfiles.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("sin->buf = bio_alloc_buf(BUFSIZ);", "sin->buf = raw bio_alloc_buf(BUFSIZ);")
    content = content.replace("sout->buf = bio_alloc_buf(BUFSIZ);", "sout->buf = raw bio_alloc_buf(BUFSIZ);")
    content = content.replace("serr->buf = bio_alloc_buf(BUFSIZ);", "serr->buf = raw bio_alloc_buf(BUFSIZ);")
    content = content.replace("int64:r1 = fflush(stdin_fp);", "int64:r1 = raw fflush(stdin_fp);")
    content = content.replace("int64:r2 = fflush(stdout_fp);", "int64:r2 = raw fflush(stdout_fp);")
    content = content.replace("int64:r3 = fflush(stderr_fp);", "int64:r3 = raw fflush(stderr_fp);")
    with open(path, "w") as f: f.write(content)

    # 3. fstr.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fstr.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:len = fputs(", "int64:len = raw fputs(")
    content = content.replace("int64:newbuf = bio_alloc_buf(", "int64:newbuf = raw bio_alloc_buf(")
    content = content.replace("int64:c = fgetc(fp);", "int64:c = raw fgetc(fp);")
    with open(path, "w") as f: f.write(content)

fix()
