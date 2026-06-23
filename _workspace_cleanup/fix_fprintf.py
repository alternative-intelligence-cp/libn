import re

with open('src/io/bio/fprintf.npk', 'r') as f:
    text = f.read()

text = re.sub(r'stack\s+byte:([a-z0-9_]+)\[4096\];', r'uint8[4096]:\1;', text)
text = re.sub(r'@cast_unchecked<int64>\(&([a-z0-9_]+)\[0\]\)', r'@cast_unchecked<int64>(\1)', text)

with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(text)
