import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

text = text.replace('slab_free(@cast_unchecked<any->>(fp))', 'libn_slab_free(@cast_unchecked<any->>(fp))')
text = text.replace('slab_free(@cast_unchecked<any->>(buf))', 'libn_slab_free(@cast_unchecked<any->>(buf))')

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)
