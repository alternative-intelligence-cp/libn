import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()
text = re.sub(r'^}$', '};', text, flags=re.MULTILINE)
with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
