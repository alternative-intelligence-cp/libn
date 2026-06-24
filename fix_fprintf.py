import re

with open('src/io/bio/fprintf.npk', 'r') as f:
    content = f.read()

def repl_fprintf(m):
    num = m.group(1)
    args = m.group(2)
    
    args_names = []
    if args:
        for arg in args.split(','):
            arg = arg.strip()
            if ':' in arg:
                args_names.append(arg.split(':')[1].strip())
            else:
                args_names.append(arg)
    pass_args = "fmt" if not args_names else f"fmt, {', '.join(args_names)}"

    return f"""pub func:fprintf{num} = int64(int64:fp, int64:fmt{', ' + args if args else ''}) {{
    drop(bio_ensure_std_init());
    int64:len = str_snprintf{num}(0i64, 0i64, {pass_args});
    if (len < FPRINTF_BUF_SIZE) {{
        stack uint8[4096]:buf;
        int64:buf_ptr = @cast_unchecked<int64>(@buf);
        drop(str_snprintf{num}(buf_ptr, FPRINTF_BUF_SIZE, {pass_args}));
        pass bio_fprint_rendered(fp, buf_ptr, len);
    }} else {{
        Result<int64>:rm = mem_malloc(len + 1i64);
        if (rm.is_error) {{ pass -1i64; }}
        int64:p = rm.value;
        drop(str_snprintf{num}(p, len + 1i64, {pass_args}));
        int64:r = bio_fprint_rendered(fp, p, len);
        drop(mem_free(p));
        pass r;
    }}
}};"""

def repl_asprintf(m):
    num = m.group(1)
    args = m.group(2)
    
    args_names = []
    if args:
        for arg in args.split(','):
            arg = arg.strip()
            if ':' in arg:
                args_names.append(arg.split(':')[1].strip())
            else:
                args_names.append(arg)
    pass_args = "fmt" if not args_names else f"fmt, {', '.join(args_names)}"

    return f"""pub func:asprintf{num} = int64(int64:out_len, int64:fmt{', ' + args if args else ''}) {{
    int64:len = str_snprintf{num}(0i64, 0i64, {pass_args});
    Result<int64>:rm = mem_malloc(len + 1i64);
    if (rm.is_error) {{ pass 0i64; }}
    int64:p = rm.value;
    drop(str_snprintf{num}(p, len + 1i64, {pass_args}));
    if (out_len != 0i64) {{ (@cast_unchecked<int64->>(out_len))[0] = len; }}
    pass p;
}};"""

pat_fprintf = r"pub func:fprintf(\d) = int64\(int64:fp, int64:fmt(?:,\s*([^\)]+))?\) \{[^\}]+\};"
content = re.sub(pat_fprintf, repl_fprintf, content, flags=re.DOTALL)

pat_asprintf = r"pub func:asprintf(\d) = int64\(int64:out_len, int64:fmt(?:,\s*([^\)]+))?\) \{[^\}]+\};"
content = re.sub(pat_asprintf, repl_asprintf, content, flags=re.DOTALL)

with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(content)
