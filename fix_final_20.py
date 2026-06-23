import os, glob

# Fix file.npk pub pub
with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()
text = text.replace('pub pub func', 'pub func')
text = text.replace('pub pub pub func', 'pub func')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

# Fix .err properly in case any missed
for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()
    if '.err' in text and '.error' not in text:
        text = text.replace('.err', '.error')
        with open(file, 'w') as f:
            f.write(text)

# Fix page_align_up / is_page_aligned
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()
text = text.replace('pass (n + PAGE_MASK) & (0i64 - PAGE_SIZE);', 'pass ((n + PAGE_MASK) & (0i64 - PAGE_SIZE));')
text = text.replace('func:is_page_aligned = NIL', 'func:is_page_aligned = bool')
with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

