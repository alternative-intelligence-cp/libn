import re

# Fix memset.npk
with open('src/mem/memset.npk', 'r') as f:
    text = f.read()
if 'pub func:compiler_fence' not in text:
    text += '\n\npub func:compiler_fence = int64() {\n    pass 0i64;\n};\n'
with open('src/mem/memset.npk', 'w') as f:
    f.write(text)

# Fix fio.npk
with open('src/io/bio/fio.npk', 'r') as f:
    text = f.read()
text = text.replace('fail FILE_EOF;', 'pass FILE_EOF;')
text = text.replace('fail EOF;', 'pass FILE_EOF;')
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(text)

# Fix fprintf.npk unused results
with open('src/io/bio/fprintf.npk', 'r') as f:
    text = f.read()
# We don't know exactly what's on 387, so we'll just sed it manually below if needed,
# or we can check what's on those lines.
