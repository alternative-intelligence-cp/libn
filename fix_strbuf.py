import re

with open('src/str/strbuf.npk', 'r') as f:
    content = f.read()

def replacer_better(match):
    num = int(match.group(1))
    
    if num > 3:
        args_def_str = ",\n                           int64:a0, int64:a1, int64:a2, int64:a3" + "".join([f", int64:a{i}" for i in range(4, num)])
    else:
        args_def_str = "".join([f", int64:a{i}" for i in range(num)])
        
    args_call = "".join([f", a{i}" for i in range(num)])
        
    return f"""pub func:strbuf_appendf{num} = int64(int64:sb, int64:fmt{args_def_str}) {{
    if (sb == 0i64) {{ pass -1i64; }}
    Result<int64>:len_res = str_snprintf{num}(0i64, 0i64, fmt{args_call});
    if (len_res.is_error) {{ pass -1i64; }}
    int64:len = len_res.value;
    if (len == 0i64) {{ pass 0i64; }}
    if (!raw strbuf_grow(sb, len)) {{ pass -1i64; }}
    StrBuf->:s = @cast_unchecked<StrBuf->>(sb);
    drop(str_snprintf{num}(s->ptr + s->len, len + 1i64, fmt{args_call}));
    s->len = s->len + len;
    pass len;
}}"""

new_content = re.sub(
    r"pub func:strbuf_appendf(\d) = int64\(int64:sb, int64:fmt.*?\) \{.*?\};",
    replacer_better,
    content,
    flags=re.DOTALL
)

with open('src/str/strbuf.npk', 'w') as f:
    f.write(new_content)
