import re

with open('src/str/strbuf.npk', 'r') as f:
    text = f.read()

# I will revert strbuf to original and run a clean script.
with open('src/str/strbuf.npk', 'r') as f:
    text = f.read()

text = re.sub(
    r'int64:r = slab_realloc\(([^)]+)\);\s*if \(r == 0i64\) \{\s*pass false;\s*\}',
    r'Result<int64>:r_res = slab_realloc(\1);\n    if (r_res.is_error) {\n        pass false;\n    }\n    int64:r = r_res.value;',
    text
)

def cast(arg):
    arg = arg.strip()
    if arg.startswith('@cast_unchecked<any->>'): return arg
    if arg == '0i64': return '@cast_unchecked<any->>(0i64)'
    if arg.isdigit() or arg.endswith('i64'): return arg
    return f'@cast_unchecked<any->>({arg})'

text = re.sub(r'mem_memcpy\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'mem_memcpy({cast(m.group(1))}, {cast(m.group(2))}, {m.group(3)})', text)
text = re.sub(r'str_strlen\(([^)]+)\)', lambda m: f'str_strlen({cast(m.group(1))})', text)

# fix str_snprintfX
# drop(str_snprintf0(tmp_ptr, STRBUF_FMT_BUF, fmt));
text = re.sub(r'str_snprintf0\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'str_snprintf0({cast(m.group(1))}, {m.group(2)}, {cast(m.group(3))})', text)

# drop(str_snprintf1(tmp_ptr, STRBUF_FMT_BUF, fmt, a0));
for i in range(1, 9):
    pattern = rf'str_snprintf{i}\(([^,]+),\s*([^,]+),\s*([^,]+),\s*(.+?)\)'
    text = re.sub(pattern, lambda m: f'str_snprintf{i}({cast(m.group(1))}, {m.group(2)}, {cast(m.group(3))}, {m.group(4)})', text)

text = re.sub(r'libn_write_all\(([^,]+),\s*([^,]+),\s*([^)]+)\)', lambda m: f'libn_write_all({m.group(1)}, {cast(m.group(2))}, {m.group(3)})', text)

with open('src/str/strbuf.npk', 'w') as f:
    f.write(text)
