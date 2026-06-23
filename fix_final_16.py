import os

with open('src/io/bio/fio.npk', 'r') as f:
    text = f.read()

imports = """use "src/syscall/syscall_numbers.npk".*;
use "src/io/bio/bio.npk".*;
"""
text = text.replace('use "src/syscall/errno.npk".*;\n', imports + 'use "src/syscall/errno.npk".*;\n')

with open('src/io/bio/fio.npk', 'w') as f:
    f.write(text)

