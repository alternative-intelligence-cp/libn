import re

filepath = "/home/randy/Workspace/REPOS/libn/src/str/strbuf.npk"

with open(filepath, 'r') as f:
    content = f.read()

# Replace raw(str_snprintfX(...)) with _!str_snprintfX(...)
content = re.sub(r'raw\((str_snprintf\d+)([^)]+)\)', r'_!\1\2', content)

# Fix the vulnerability
def repl_appendf(m):
    # m.group(1) is the n assignment and check
    # m.group(2) is the strbuf_append_bytes line
    # We replace the strbuf_append_bytes line
    snprintf_call = m.group(1)
    
    # We need to insert the copy_len clamping logic
    # and replace strbuf_append_bytes with _!strbuf_append_bytes
    replacement = snprintf_call + """
    int64:copy_len = is n < (STRBUF_FMT_BUF - 1i64) : n : (STRBUF_FMT_BUF - 1i64);
    if !_!strbuf_append_bytes(sb, tmp_ptr, copy_len) { pass(-1i64); }"""
    return replacement

# Match:
#    int64:n = _!str_snprintfX(...);
#    if n == 0i64 { pass(0i64); }
#    if !strbuf_append_bytes(sb, tmp_ptr, n) { pass(-1i64); }
pattern = r'(int64:n = _!str_snprintf\d+\(.*?\);\s+if n == 0i64 \{ pass\(0i64\); \})\s+if !strbuf_append_bytes\(sb, tmp_ptr, n\) \{ pass\(-1i64\); \}'
content = re.sub(pattern, repl_appendf, content)

with open(filepath, 'w') as f:
    f.write(content)

print("strbuf.npk fixed")
