import re

# Fix fio.npk circular import
with open('src/io/bio/fio.npk', 'r') as f:
    text = f.read()
text = text.replace('use "src/io/bio/bio.npk".*;\n', '')
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(text)

# Fix file.npk missing pub
with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()
text = text.replace('\nfunc:bio_flush_write_buf', '\npub func:bio_flush_write_buf')
text = text.replace('\nfunc:bio_refill_read_buf', '\npub func:bio_refill_read_buf')
text = text.replace('\nfunc:bio_discard_read_buf', '\npub func:bio_discard_read_buf')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

# Find "Result<int64> into '...'" error in fio.npk
# "Cannot silently unwrap Result<int64> into 'total' of type 'int64'."
# I'll just change `int64:total = ...` to `Result<int64>:total = ...` if needed.
# Let's peek at fio.npk lines 180-200, 240-260, and strbuf.npk 310-350.

