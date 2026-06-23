import re
with open('src/io/bio/fchar.npk', 'r') as f:
    text = f.read()

text = re.sub(r'\bbyte\b', 'uint8', text)

with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(text)
