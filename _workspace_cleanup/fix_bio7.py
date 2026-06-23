import os
import re

def fix():
    # 1. file.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("func:bio_discard_read_buf", "pub func:bio_discard_read_buf")
    content = content.replace("func:bio_refill_read_buf", "pub func:bio_refill_read_buf")
    with open(path, "w") as f: f.write(content)

    # 2. fio.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fio.npk"
    with open(path, "r") as f: content = f.read()
    if "src/syscall/syscall_numbers.npk" not in content:
        content = content.replace('use "src/syscall/syscall.npk".*;', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;')
    
    # 3. fchar.npk (add syscall_numbers if needed)
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk"
    with open(path, "r") as f: content = f.read()
    if "src/syscall/syscall_numbers.npk" not in content:
        content = content.replace('use "src/syscall/syscall.npk".*;', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;')
    with open(path, "w") as f: f.write(content)
    
    # 4. memutil.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/memutil.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:candidate = mem_memchr(", "int64:candidate = raw mem_memchr(")
    with open(path, "w") as f: f.write(content)

    # 5. exec.npk
    path = "/home/randy/Workspace/REPOS/libn/src/proc/exec.npk"
    with open(path, "r") as f: content = f.read()
    # It had an error: Line 160: execve(&candidate[0] as int64, argv, envp);
    # Nitpick doesn't support &candidate[0] as int64, it's @cast_unchecked<int64>(@candidate[0])
    content = content.replace("&candidate[0] as int64", "@cast_unchecked<int64>(@candidate[0])")
    with open(path, "w") as f: f.write(content)
    
fix()
