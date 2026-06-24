import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

def cast(arg):
    arg = arg.strip()
    if arg.startswith('@cast_unchecked<any->>'): return arg
    if arg == '0i64': return '@cast_unchecked<any->>(0i64)'
    if arg.isdigit() or arg.endswith('i64'): return arg
    return f'@cast_unchecked<any->>({arg})'

# Replace str_strlen
text = re.sub(r'str_strlen\(([^)]+)\)', lambda m: f'str_strlen({cast(m.group(1))})', text)

# mem_memcpy(dst, src, len)
text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memcpy({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)

# mem_memcmp(a, b, len) - mem_memcmp EXPECTS int64! Do NOT cast to any->!
# Wait, mem_memcmp is int64(int64:a, int64:b, int64:n). So no change.

# mem_memmem(haystack, hlen, needle, nlen) - expects int64! Do NOT cast to any->!

# mem_memchr(s, c, len) - expects int64! Do NOT cast to any->!

# mem_memrchr(s, c, len) - expects int64! Do NOT cast to any->!

# mem_equal(a, b, len) - expects int64! Do NOT cast to any->!

# strbuf_append_bytes(sb, ptr, len) => strbuf_append_bytes was probably changed to expect any->! Let's check strbuf.npk.
# Actually, I'll just cast ptr.
# text = re.sub(r'strbuf_append_bytes\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'strbuf_append_bytes({m.group(1)}, {cast(m.group(2))}, {m.group(3)})', text)
# Wait, strbuf_append_bytes in strbuf.npk: `pub func:strbuf_append_bytes = NIL(int64:sb, int64:bytes, int64:len)`
# If I didn't change strbuf.npk, it expects int64!
# Did I change strbuf.npk? Let me grep strbuf_append_bytes.

# libn_write_all(fd, buf, len) => buf expects any->
text = re.sub(r'libn_write_all\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'libn_write_all({m.group(1)}, {cast(m.group(2))}, {m.group(3)})', text)

# fwrite(ptr, size, nitems, stream) => ptr expects any->
text = re.sub(r'fwrite\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'fwrite({cast(m.group(1))}, {m.group(2)}, {m.group(3)}, {m.group(4)})', text)

# slab_alloc_zero
text = text.replace('libn_slab_alloc_zero', 'slab_alloc_zero')

# Add missing imports
if 'use "../syscall/syscall.npk".*;' not in text:
    text = text.replace('use "../syscall/errno.npk".*;\n', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/slab.npk".*;\nuse "../str/strchr.npk".*;\nuse "../str/strcmp.npk".*;\n')

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

