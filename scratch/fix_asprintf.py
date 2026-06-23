import os
import re

filepath = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
with open(filepath, 'r') as f:
    content = f.read()

# Replace asprintf0 to asprintf4
# From:
# pub func:asprintfX = int64(int64:out_len, int64:fmt, ...) {
#     stack uint8[4096]:tmp; ...
#     pass(p);
# }
# To:
# pub func:asprintfX = int64(int64:out_len, int64:fmt, ...) {
#     int64:sb = _!strbuf_new();
#     _?strbuf_appendfX(sb, fmt, ...);
#     int64:p = _!strbuf_finish(sb);
#     if out_len != 0i64 { <-(out_len => int64->) = _!str_strlen(p); }
#     pass(p);
# }

def repl_asprintf(m):
    sig = m.group(1) # pub func:asprintfX = int64(int64:out_len, int64:fmt, ...)
    num = m.group(2) # X
    args = m.group(3) # a0, a1 ...
    
    body = f"""    int64:sb = _!strbuf_new();
    _?strbuf_appendf{num}(sb, fmt{', ' + args if args else ''});
    int64:p = _!strbuf_finish(sb);
    if out_len != 0i64 {{ <-(out_len => int64->) = _!str_strlen(p); }}
    pass(p);
}}"""
    return f"{sig} {{\n{body}"

pattern = r'(pub func:asprintf(\d) = int64\(int64:out_len, int64:fmt(?:,\s*(.*?))?\) \{)[\s\S]*?pass\(p\);\n\}'
content = re.sub(pattern, repl_asprintf, content)

# I also need to add use "src/str/strbuf.npk".*; if not there
if 'use "src/str/strbuf.npk".*;' not in content:
    content = content.replace('use "src/str/strfmt.npk".*;\n', 'use "src/str/strfmt.npk".*;\nuse "src/str/strbuf.npk".*;\n')

with open(filepath, 'w') as f:
    f.write(content)
print("fprintf.npk asprintf fixed")
