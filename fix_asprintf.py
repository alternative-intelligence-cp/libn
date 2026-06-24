import re

with open('src/io/bio/fprintf.npk', 'r') as f:
    content = f.read()

def replacer(match):
    num = match.group(1)
    args = match.group(2)
    fmt_call_args = match.group(3)
    
    return f"""pub func:asprintf{num} = int64(int64:out_len, int64:fmt{args}) {{
    Result<int64>:len_res = str_snprintf{num}(0i64, 0i64, fmt{fmt_call_args});
    if (len_res.is_error) {{ pass -1i64; }}
    int64:len = len_res.value;
    int64:p = raw mem_malloc(len + 1i64);
    if (p == 0i64) {{ pass 0i64; }}
    drop(str_snprintf{num}(p, len + 1i64, fmt{fmt_call_args}));
    if (out_len != 0i64) {{ (@cast_unchecked<int64->>(out_len))[0] = len; }}
    pass p;
}};"""

# We need to match the full function bodies.
pattern = re.compile(
    r"pub func:asprintf(\d) = int64\(int64:out_len, int64:fmt(.*?)\) \{(.*?)\};",
    re.DOTALL
)

# Wait, fmt_call_args needs to be parsed from the original. 
# But it's easier to just construct it.
def replacer_better(match):
    num = int(match.group(1))
    
    args_def = "".join([f", int64:a{i}" for i in range(num)])
    args_call = "".join([f", a{i}" for i in range(num)])
    
    # We might need to split arguments into lines if it's too long, but Nitpick doesn't care.
    if num > 3:
        args_def_str = ",\n                           int64:a0, int64:a1, int64:a2, int64:a3" + "".join([f", int64:a{i}" for i in range(4, num)])
    else:
        args_def_str = "".join([f", int64:a{i}" for i in range(num)])
        
    return f"""pub func:asprintf{num} = int64(int64:out_len, int64:fmt{args_def_str}) {{
    Result<int64>:len_res = str_snprintf{num}(0i64, 0i64, fmt{args_call});
    if (len_res.is_error) {{ pass -1i64; }}
    int64:len = len_res.value;
    int64:p = raw mem_malloc(len + 1i64);
    if (p == 0i64) {{ pass 0i64; }}
    drop(str_snprintf{num}(p, len + 1i64, fmt{args_call}));
    if (out_len != 0i64) {{ (@cast_unchecked<int64->>(out_len))[0] = len; }}
    pass p;
}}"""

new_content = re.sub(
    r"pub func:asprintf(\d) = int64\(int64:out_len, int64:fmt.*?\) \{.*?\};",
    replacer_better,
    content,
    flags=re.DOTALL
)

with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(new_content)
