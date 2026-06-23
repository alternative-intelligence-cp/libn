import re

def rewrite(filepath, replacements):
    with open(filepath, 'r') as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(text)

rewrite('src/fs/path.npk', [
    ('int64:end = len;', 'int64:end_idx = len;'),
    ('while (end > 1i64', 'while (end_idx > 1i64'),
    ('p[end - 1i64]', 'p[end_idx - 1i64]'),
    ('end = end - 1i64;', 'end_idx = end_idx - 1i64;'),
    ('int64:i = end - 1i64;', 'int64:i = end_idx - 1i64;')
])

rewrite('src/math/math.npk', [
    ('int64:limit = ', 'int64:limit_val = '),
    ('while (i < limit)', 'while (i < limit_val)')
])

rewrite('src/io/write.npk', [
    ('&@cast_unchecked<int64>(b[0])', '@cast_unchecked<int64>(&b[0])')
])

