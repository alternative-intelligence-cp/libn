import sys

files = [
    'src/io/bio/file.npk',
    'src/mem/mmap.npk',
    'src/mem/slab.npk'
]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    content = content.replace('slab_free(0i64, ', 'slab_free(')
    with open(f, 'w') as file:
        file.write(content)
print("done")
