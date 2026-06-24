import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

def wrap(arg):
    arg = arg.strip()
    if arg.startswith('@cast'): return arg
    if arg.startswith('"'): return arg
    return f"@cast_unchecked<any->>({arg})"

def repl_1(m):
    return f"{m.group(1)}({wrap(m.group(2))})"

def repl_2(m):
    return f"{m.group(1)}({wrap(m.group(2))}, {wrap(m.group(3))})"

def repl_3(m):
    return f"{m.group(1)}({wrap(m.group(2))}, {wrap(m.group(3))}, {m.group(4)})"

text = re.sub(r'\b(str_strlen|str_parse_i64|str_parse_u64)\s*\(\s*([^)]+)\s*\)', repl_1, text)
text = re.sub(r'\b(str_strcmp|str_strcasecmp|str_casecmp_prefix)\s*\(\s*([^,]+),\s*([^)]+)\s*\)', repl_2, text)
text = re.sub(r'\b(str_strncmp|str_strncasecmp|mem_memcpy)\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\s*\)', repl_3, text)

# For strview_print, it needs io_write_n or io_write_str
# Actually, the compile error said libn_write_all was missing. So I should add back `use "../syscall/syscall.npk".*;`
# Wait, strview.npk already has `use "../syscall/syscall.npk".*;`! But `libn_write_all` is defined in `src/syscall/syscall.npk`.
# Let's check if it does.

with open('src/str/strview.npk', 'w') as f:
    f.write(text)
