import os
import re

# 1. slab.npk
with open('src/mem/slab.npk', 'r') as f:
    code = f.read()
# Revert cls_r
code = code.replace(
    'Result<int64>:cls_r = slab_class_for_size(n);\n    int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; }',
    'int64:cls = slab_class_for_size(n);'
)
with open('src/mem/slab.npk', 'w') as f:
    f.write(code)

# 2. stdfiles.npk
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
# Unused Result<NIL>
code = code.replace('Result<NIL>:_nil_r = bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init(); drop(_nil_r);')
# stdin_buf and stdout_buf
code = re.sub(r'int64:stdin_buf = mem_malloc\(BUFSIZ\);', r'Result<int64>:r_in = mem_malloc(BUFSIZ);\n    int64:stdin_buf = 0i64;\n    if (!r_in.is_error) { stdin_buf = r_in.value; }', code)
code = re.sub(r'int64:stdout_buf = mem_malloc\(BUFSIZ\);', r'Result<int64>:r_out = mem_malloc(BUFSIZ);\n    int64:stdout_buf = 0i64;\n    if (!r_out.is_error) { stdout_buf = r_out.value; }', code)
# `r` unwrap (probably bio_flush_stdout/stderr)
code = code.replace('int64:r = fputs(s, stdout_fp);', 'Result<int64>:r_f = fputs(s, stdout_fp);\n    int64:r = 0i64; if (!r_f.is_error) { r = r_f.value; } else { r = FILE_EOF; }')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# 3. file.npk and fprintf.npk and fchar.npk
for p in ['src/io/bio/file.npk', 'src/io/bio/fprintf.npk', 'src/io/bio/fchar.npk', 'src/io/bio/fio.npk', 'src/io/bio/fopen.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        code = code.replace('Result<NIL>:_nil_r = bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init(); drop(_nil_r);')
        # Fix parse_ok
        code = re.sub(r'Result<int64>:parse_ok_r = bio_parse_mode\((.*?)\);', r'Result<int64>:parse_ok_r = bio_parse_mode(\1);\n    int64:parse_ok = 0i64;\n    if (!parse_ok_r.is_error) { parse_ok = parse_ok_r.value; }', code)
        code = code.replace('int64:parse_ok = 0i64; if (!parse_ok_r.is_error) { parse_ok = parse_ok_r.value; } if (parse_ok == 0i64)', 'if (parse_ok == 0i64)')
        # Fix fp missing
        code = code.replace('Result<int64>:fp_r = bio_alloc_file(); int64:fp = 0i64; if (!fp_r.is_error) { fp = fp_r.value; }', 'Result<int64>:fp_r = bio_alloc_file();\n    int64:fp = 0i64;\n    if (!fp_r.is_error) { fp = fp_r.value; }')
        
        # fix missing newbuf wrap in file.npk
        code = re.sub(r'int64:newbuf = mem_malloc\((.*?)\);', r'Result<int64>:nb_r = mem_malloc(\1);\n    int64:newbuf = 0i64;\n    if (!nb_r.is_error) { newbuf = nb_r.value; }', code)
        # fix value without check in file.npk
        code = code.replace('pass r.value;', 'if (!r.is_error) { pass r.value; } pass 0i64;')
        
        with open(p, 'w') as f:
            f.write(code)

# 4. strlen.npk has_nul_byte
with open('src/str/strlen.npk', 'r') as f:
    code = f.read()
code = code.replace('has_nul_byte', 'has_zero_byte')
code = code.replace('has_zero_byte(w) != 0i64', 'has_zero_byte(w) != 0i64') # Already fine? Let's check bitwise
code = code.replace('has_zero_byte(w)', '(has_zero_byte(w) != 0i64)')
# If it becomes ((has_zero_byte(w) != 0i64) != 0i64), it's fine.
with open('src/str/strlen.npk', 'w') as f:
    f.write(code)

# 5. strerror.npk
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
# Replace ALL err_msg_0 to err_msg_X to prevent undefined
code = re.sub(r'err_msg_\d+', lambda m: m.group(0) + '_Z', code) # Make them unique
matches = re.findall(r'\{\s*(-?\d+i64),\s*@cast_unchecked<int64>\("([^"]+)"\)\s*\}', code)
declarations = []
for i, match in enumerate(matches):
    errnum = match[0]
    msg = match[1]
    var_name = f'err_msg_Z{i}'
    declarations.append(f'fixed string:{var_name} = "{msg}";')
    code = code.replace(f'@cast_unchecked<int64>("{msg}")', f'@cast_unchecked<int64>(@{var_name})')
if len(declarations) > 0:
    code = code.replace('fixed ErrEntry[]:errno_table = [', '\n'.join(declarations) + '\n\nfixed ErrEntry[]:errno_table = [')
# num_len unwrap
code = code.replace(
    'int64:num_len = str_itoa(errnum, @cast_unchecked<int64>(@num[0]), 24i64);',
    'Result<int64>:num_len_r = str_itoa(errnum, @cast_unchecked<int64>(@num[0]), 24i64);\n    int64:num_len = 0i64; if (!num_len_r.is_error) { num_len = num_len_r.value; }'
)
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 6. strfmt.npk: str_snprintf5 and str_snprintf7
with open('src/str/strfmt.npk', 'r') as f:
    code = f.read()
if 'str_snprintf5' not in code:
    code += '''\npub func:str_snprintf5 = int64(int64:buf, int64:size, int64:fmt, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5) {
    int64[]:args = [ a1, a2, a3, a4, a5 ];
    pass str_vsnprintf(buf, size, fmt, @cast_unchecked<int64>(@args[0]));
};\n'''
if 'str_snprintf7' not in code:
    code += '''\npub func:str_snprintf7 = int64(int64:buf, int64:size, int64:fmt, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6, int64:a7) {
    int64[]:args = [ a1, a2, a3, a4, a5, a6, a7 ];
    pass str_vsnprintf(buf, size, fmt, @cast_unchecked<int64>(@args[0]));
};\n'''
with open('src/str/strfmt.npk', 'w') as f:
    f.write(code)

print("Applied final_resolution_2.py")
