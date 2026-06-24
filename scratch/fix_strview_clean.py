import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

# Add missing imports (just one line so line numbers don't shift by much, but whatever)
if 'use "../syscall/syscall.npk".*;' not in text:
    text = text.replace('use "../syscall/errno.npk".*;\n', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/slab.npk".*;\nuse "../str/strchr.npk".*;\nuse "../str/strcmp.npk".*;\n')

# Fix slab_alloc_zero
text = text.replace('libn_slab_alloc_zero', 'slab_alloc_zero')

# Replace str_strlen calls to cast argument to any->
text = re.sub(r'str_strlen\(([^)]+)\)', r'str_strlen(@cast_unchecked<any->>(\1))', text)

# mem_memcpy(dst, src, len) -> mem_memcpy(@cast_unchecked<any->>(dst), @cast_unchecked<any->>(src), len)
text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memcpy(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

# mem_memcmp(a, b, len)
text = re.sub(r'mem_memcmp\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memcmp(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

# mem_memmem(haystack, hlen, needle, nlen)
text = re.sub(r'mem_memmem\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memmem(@cast_unchecked<any->>(\1), \2, @cast_unchecked<any->>(\3), \4)', text)

# mem_memchr(s, c, len)
text = re.sub(r'mem_memchr\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memchr(@cast_unchecked<any->>(\1), \2, \3)', text)

# mem_memrchr(s, c, len)
text = re.sub(r'mem_memrchr\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_memrchr(@cast_unchecked<any->>(\1), \2, \3)', text)

# mem_equal(a, b, len) => Actually, does mem_equal expect any->? YES it was changed in memutil!
text = re.sub(r'mem_equal\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'mem_equal(@cast_unchecked<any->>(\1), @cast_unchecked<any->>(\2), \3)', text)

# strbuf_append_bytes(sb, ptr, len) => wait, strbuf.npk probably takes any-> now for ptr!
text = re.sub(r'strbuf_append_bytes\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'strbuf_append_bytes(\1, @cast_unchecked<any->>(\2), \3)', text)

# libn_write_all(fd, buf, len) => buf needs any->
text = re.sub(r'libn_write_all\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'libn_write_all(\1, @cast_unchecked<any->>(\2), \3)', text)

# fwrite(ptr, size, nitems, stream) => ptr needs any->
text = re.sub(r'fwrite\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', r'fwrite(@cast_unchecked<any->>(\1), \2, \3, \4)', text)

# Any nested @cast_unchecked<any->>(@cast_unchecked<any->>(...)) from running this multiple times/on already replaced things?
text = text.replace('@cast_unchecked<any->>(@cast_unchecked<any->>(', '@cast_unchecked<any->>(').replace('))', ')')

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

