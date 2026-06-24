import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

# I will use a simple regex replacing function that prevents nesting.
def cast(arg):
    arg = arg.strip()
    if arg.startswith('@cast_unchecked<any->>'): return arg
    if arg == '0i64': return '@cast_unchecked<any->>(0i64)'
    if arg.isdigit() or arg.endswith('i64'): return arg
    return f'@cast_unchecked<any->>({arg})'

# Fix str_strlen calls to cast argument to any->
text = re.sub(r'str_strlen\(([^)]+)\)', lambda m: f'str_strlen({cast(m.group(1))})', text)

# mem_memcpy(dst, src, len)
text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memcpy({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)

# mem_memcmp(a, b, len)
text = re.sub(r'mem_memcmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memcmp({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)

# mem_memmem(haystack, hlen, needle, nlen)
text = re.sub(r'mem_memmem\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memmem({cast(m.group(1))}, {m.group(2)}, {cast(m.group(3))}, {m.group(4)})', text)

# mem_memchr(s, c, len)
text = re.sub(r'mem_memchr\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memchr({cast(m.group(1))}, {m.group(2)}, {m.group(3)})', text)

# mem_memrchr(s, c, len)
text = re.sub(r'mem_memrchr\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memrchr({cast(m.group(1))}, {m.group(2)}, {m.group(3)})', text)

# mem_equal(a, b, len)
text = re.sub(r'mem_equal\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_equal({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)

# strbuf_append_bytes(sb, ptr, len)
text = re.sub(r'strbuf_append_bytes\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'strbuf_append_bytes({m.group(1)}, {cast(m.group(2))}, {m.group(3)})', text)

# libn_write_all(fd, buf, len)
text = re.sub(r'libn_write_all\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'libn_write_all({m.group(1)}, {cast(m.group(2))}, {m.group(3)})', text)

# libn_slab_alloc_zero -> slab_alloc_zero
text = text.replace('libn_slab_alloc_zero', 'slab_alloc_zero')

# Add missing imports (just one line so line numbers don't shift by much, but whatever)
if 'use "../syscall/syscall.npk".*;' not in text:
    text = text.replace('use "../syscall/errno.npk".*;\n', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/slab.npk".*;\nuse "../str/strchr.npk".*;\nuse "../str/strcmp.npk".*;\n')

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

