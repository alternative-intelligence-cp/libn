import os, glob

# Fix file.npk bio_refill_read_buf space
with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()
text = text.replace('func : bio_refill_read_buf', 'pub func:bio_refill_read_buf')
text = text.replace('func:bio_discard_read_buf', 'pub func:bio_discard_read_buf')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('pass(0i64);', 'exit 0i64;')
text = text.replace('pass(true);', 'exit 0i64;')
text = text.replace('pass;', 'exit 0i64;')
with open('test_all.npk', 'w') as f:
    f.write(text)

