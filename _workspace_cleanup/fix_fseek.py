import re
with open("src/io/bio/fseek.npk", "r") as f:
    content = f.read()

content = content.replace('(pos as *int64)[0] = p;', '@cast_unchecked<int64->>(pos)[0] = p;')
content = content.replace('int64:target = (pos as *int64)[0];', 'int64:target = @cast_unchecked<int64->>(pos)[0];')

with open("src/io/bio/fseek.npk", "w") as f:
    f.write(content)
