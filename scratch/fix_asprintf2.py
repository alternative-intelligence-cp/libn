import os
import re

filepath = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
with open(filepath, 'r') as f:
    content = f.read()

# Replace double braces and types in calls
def fix_body(m):
    sig = m.group(1) # pub func:asprintfX = ... {
    
    # Extract arguments without types
    arg_match = re.search(r'pub func:asprintf\d = int64\(int64:out_len, int64:fmt(?:,\s*(.*?))?\)\s*\{', sig)
    raw_args = arg_match.group(1) if arg_match.group(1) else ""
    
    # Strip types like int64:a0 -> a0
    clean_args = []
    if raw_args:
        for p in raw_args.split(','):
            p = p.strip()
            if ':' in p:
                clean_args.append(p.split(':')[1].strip())
            else:
                clean_args.append(p)
    args_str = ", ".join(clean_args)
    if args_str:
        args_str = ", " + args_str
    
    num = re.search(r'asprintf(\d)', sig).group(1)
    
    body = f"""
    int64:sb = _!strbuf_new();
    _?strbuf_appendf{num}(sb, fmt{args_str});
    int64:p = _!strbuf_finish(sb);
    if out_len != 0i64 {{ <-(out_len => int64->) = _!str_strlen(p); }}
    pass(p);
}}"""
    return f"{sig}{body}"

pattern = r'(pub func:asprintf\d = int64\(int64:out_len, int64:fmt(?:.*?)\) \{) \{\s*int64:sb = _!strbuf_new\(\);\s*_!?[?]?strbuf_appendf\d\(sb, fmt.*?\);\s*int64:p = _!strbuf_finish\(sb\);\s*if out_len != 0i64 \{ <-\(out_len => int64->\) = _!str_strlen\(p\); \}\s*pass\(p\);\s*\}'
content = re.sub(pattern, fix_body, content)

with open(filepath, 'w') as f:
    f.write(content)
print("fprintf.npk syntax fixed")
