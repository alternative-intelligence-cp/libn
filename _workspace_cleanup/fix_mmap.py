import re
with open("src/mem/mmap.npk", "r") as f:
    content = f.read()

content = content.replace('sys(MADVISE, addr, length, advice)', 'sys(MADVISE, addr, length, advice, 0i64, 0i64, 0i64)')
content = content.replace('sys(MREMAP, addr, old_len, new_len, 0i64)', 'sys(MREMAP, addr, old_len, new_len, 0i64, 0i64, 0i64)')
content = content.replace('sys(MSYNC, addr, length, flags)', 'sys(MSYNC, addr, length, flags, 0i64, 0i64, 0i64)')

with open("src/mem/mmap.npk", "w") as f:
    f.write(content)
