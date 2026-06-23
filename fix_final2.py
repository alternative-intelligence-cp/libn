import re

def rewrite(filepath, replacements):
    with open(filepath, 'r') as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(text)

rewrite('src/str/strlen.npk', [
    ('int64:limit)', 'int64:limit_val)'),
    ('limit + 1i64', 'limit_val + 1i64'),
    ('n > limit', 'n > limit_val')
])

rewrite('src/mem/memutil.npk', [
    ('int64:limit = hlen - nlen;', 'int64:limit_val = hlen - nlen;'),
    ('i <= limit', 'i <= limit_val'),
    ('offset > limit', 'offset > limit_val')
])

rewrite('src/math/math.npk', [
    ('int64:limit_val = INT64_MAX / abs_b;', 'int64:limit_val = INT64_MAX / abs_b;'),
    ('if (abs_a > limit)', 'if (abs_a > limit_val)')
])

rewrite('src/io/bio/file.npk', [
    ('oflags[0] = has_plus ? O_RDWR : O_RDONLY;', 'if (has_plus) { oflags[0] = O_RDWR; } else { oflags[0] = O_RDONLY; }')
])

rewrite('src/io/write.npk', [
    ('@cast_unchecked<int64>(&b[0])', '@cast_unchecked<int64>(&b)')
])

