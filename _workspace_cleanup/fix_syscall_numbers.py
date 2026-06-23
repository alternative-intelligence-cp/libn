import re

with open("src/syscall/syscall_numbers.npk", "r") as f:
    content = f.read()

content = content.replace("pub fixed int64:MMAP", "pub fixed int64:SYS_MMAP")
content = content.replace("pub fixed int64:MPROTECT", "pub fixed int64:SYS_MPROTECT")
content = content.replace("pub fixed int64:MUNMAP", "pub fixed int64:SYS_MUNMAP")
content = content.replace("pub fixed int64:MREMAP", "pub fixed int64:SYS_MREMAP")
content = content.replace("pub fixed int64:MADVISE", "pub fixed int64:SYS_MADVISE")

with open("src/syscall/syscall_numbers.npk", "w") as f:
    f.write(content)

def add_import(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    if 'use "src/syscall/syscall_numbers.npk".*;' not in content:
        content = content.replace('use "src/syscall/syscall.npk".*;\n', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;\n')
    with open(filepath, "w") as f:
        f.write(content)

add_import("src/io/bio/fio.npk")
add_import("src/io/bio/fchar.npk")
