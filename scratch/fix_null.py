import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()
text = text.replace("NULL", "@cast_unchecked<any->>(0i64)")
with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

with open('src/mem/memcpy.npk', 'r') as f:
    text = f.read()
text = text.replace("NULL", "@cast_unchecked<any->>(0i64)")
with open('src/mem/memcpy.npk', 'w') as f:
    f.write(text)
