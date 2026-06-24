import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

text = text.replace('libn_slab_alloc_zero', 'slab_alloc_zero')

# any mem_memcpy or other functions in file.npk?
# let's just write back for now
with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)
