with open('src/mem/memset.npk', 'r') as f:
    text = f.read()

text = text.replace("drop(memset(ptr, c, n));", "int8->:_discard = memset(ptr, c, n);")

with open('src/mem/memset.npk', 'w') as f:
    f.write(text)

