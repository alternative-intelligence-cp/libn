import re
with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

text = re.sub(r'pass raw (sys(?:!!?)?\([^)]+\));', r'Result<int64>:r = \1;\n    pass r;', text)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)
