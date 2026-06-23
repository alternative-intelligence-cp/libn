import os
import re

def fix():
    # 1. file.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'([a-zA-Z0-9_]+)\s*=>\s*FILE->', r'@cast_unchecked<FILE->>(\1)', content)
    with open(path, "w") as f: f.write(content)

    # 2. fopen.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'([a-zA-Z0-9_]+)\s*=>\s*FILE->', r'@cast_unchecked<FILE->>(\1)', content)
    content = content.replace("if ((raw libn_fcntl(fd, F_GETFL, 0i64)) & O_APPEND != 0i64) {", 
                              "if (((raw libn_fcntl(fd, F_GETFL, 0i64)) & O_APPEND) != 0i64) {")
    with open(path, "w") as f: f.write(content)

    # 3. fseek.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fseek.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'([a-zA-Z0-9_]+)\s*=>\s*FILE->', r'@cast_unchecked<FILE->>(\1)', content)
    with open(path, "w") as f: f.write(content)

    # 4. memutil.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/memutil.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("if (has_zero_byte(v)) {", "if (raw has_zero_byte(v)) {")
    content = content.replace("if (mem_memcmp(candidate, needle, nlen) == 0i64) {", "if ((raw mem_memcmp(candidate, needle, nlen)) == 0i64) {")
    with open(path, "w") as f: f.write(content)

    # 5. mmap.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("drop libn_munmap(base, total_size);", "Result<int64>:r = libn_munmap(base, total_size);")
    with open(path, "w") as f: f.write(content)

fix()
