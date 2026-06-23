import os
import re

def fix():
    # 1. strerror.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:msg = strerror(", "int64:msg = raw strerror(")
    content = content.replace("int64:msg_len = str_strlen(", "int64:msg_len = raw str_strlen(")
    with open(path, "w") as f: f.write(content)

    # 2. fopen.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("func:bio_init_stream = Result<int64>(", "func:bio_init_stream = int64(")
    with open(path, "w") as f: f.write(content)

    # 3. file.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("pub func:bio_discard_read_buf = Result<int64>(", "pub func:bio_discard_read_buf = int64(")
    content = content.replace("pub func:bio_refill_read_buf = Result<int64>(", "pub func:bio_refill_read_buf = int64(")
    content = content.replace("int64:res = libn_write(", "int64:res = raw libn_write(")
    content = content.replace("int64:res = libn_lseek(", "int64:res = raw libn_lseek(")
    content = content.replace("int64:res = libn_read(", "int64:res = raw libn_read(")
    with open(path, "w") as f: f.write(content)

    # 4. fseek.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fseek.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("if (libn_lseek(", "if (raw libn_lseek(")
    with open(path, "w") as f: f.write(content)

    # 5. memutil.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/memutil.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:r = mem_memcmp(", "int64:r = raw mem_memcmp(")
    content = content.replace("int64:tword = replicate_byte(", "int64:tword = raw replicate_byte(")
    with open(path, "w") as f: f.write(content)

    # 6. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace('raw str_strlen(@cast_unchecked<int64>("-9223372036854775808"))', 'raw str_strlen(@cast_unchecked<int64>(@"-9223372036854775808"))')
    content = content.replace('@cast_unchecked<int64>("-9223372036854775808")', '@cast_unchecked<int64>(@"-9223372036854775808")')
    content = content.replace('@cast_unchecked<int64>(min_int)', '@cast_unchecked<int64>(@"-9223372036854775808")')
    with open(path, "w") as f: f.write(content)

    # 7. strtok.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strtok.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("!raw charset_test(", "(raw charset_test(")
    # wait, !raw charset_test should be (raw charset_test(...) == false)
    content = re.sub(r'!raw charset_test\((.*?)\)', r'(raw charset_test(\1) == false)', content)
    # also raw charset_test without ! should be == true
    content = re.sub(r'([^\!])raw charset_test\((.*?)\)', r'\1(raw charset_test(\2) == true)', content)
    with open(path, "w") as f: f.write(content)

    # 8. strchr.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strchr.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'!raw charset_test\((.*?)\)', r'(raw charset_test(\1) == false)', content)
    content = re.sub(r'([^\!])raw charset_test\((.*?)\)', r'\1(raw charset_test(\2) == true)', content)
    with open(path, "w") as f: f.write(content)

fix()
