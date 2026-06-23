import os

# 1. file.npk
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
for func in ['bio_alloc_file', 'bio_free_file', 'bio_alloc_buf', 'bio_free_buf', 'bio_flush_write_buf', 'bio_discard_read_buf', 'bio_refill_read_buf', 'bio_parse_mode']:
    code = code.replace(f'func:{func}', f'pub func:{func}')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

# 2. stdfiles.npk
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
code = code.replace('(g_stdin_file)', '(@g_stdin_file)')
code = code.replace('(g_stdout_file)', '(@g_stdout_file)')
code = code.replace('(g_stderr_file)', '(@g_stderr_file)')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# 3. strlen.npk
with open('src/str/strlen.npk', 'r') as f:
    code = f.read()
code = code.replace('((s + i) & 7i64 != 0i64)', '(((s + i) & 7i64) != 0i64)')
code = code.replace('has_nul_byte', 'has_zero_byte')
with open('src/str/strlen.npk', 'w') as f:
    f.write(code)

# 4. strconv.npk
with open('src/str/strconv.npk', 'r') as f:
    code = f.read()
code = code.replace('drop errno_clear();', 'drop libn_errno_set(0i64);')
if 'use "src/mem/memcpy.npk".*;' not in code:
    code = 'use "src/mem/memcpy.npk".*;\nuse "src/mem/mmap.npk".*;\n' + code
with open('src/str/strconv.npk', 'w') as f:
    f.write(code)

# 5. fchar.npk
with open('src/io/bio/fchar.npk', 'r') as f:
    code = f.read()
if 'use "src/syscall/syscall_numbers.npk".*;' not in code:
    code = 'use "src/syscall/syscall_numbers.npk".*;\n' + code
with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(code)

# 6. strfmt.npk
with open('src/str/strfmt.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'fixed int64:DIGITS_LOWER = @cast_unchecked<int64>(@"0123456789abcdef"[0]);',
    'fixed string:LOWER_STR = "0123456789abcdef";\nfixed int64:DIGITS_LOWER = @cast_unchecked<int64>(@LOWER_STR);'
)
code = code.replace(
    'fixed int64:DIGITS_UPPER = @cast_unchecked<int64>(@"0123456789ABCDEF"[0]);',
    'fixed string:UPPER_STR = "0123456789ABCDEF";\nfixed int64:DIGITS_UPPER = @cast_unchecked<int64>(@UPPER_STR);'
)
code = code.replace(
    'sptr = @cast_unchecked<int64>(@"(null)"[0]);',
    'fixed string:NULL_STR = "(null)";\n                sptr = @cast_unchecked<int64>(@NULL_STR);'
)

func5 = """
pub func:str_snprintf5 = int64(int64:buf, int64:buf_size, int64:fmt, int64:a0, int64:a1, int64:a2, int64:a3, int64:a4) {
    stack int64[5]:a;
    a[0] = a0; a[1] = a1; a[2] = a2; a[3] = a3; a[4] = a4;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 5i64);
};
"""
func7 = """
pub func:str_snprintf7 = int64(int64:buf, int64:buf_size, int64:fmt, int64:a0, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {
    stack int64[7]:a;
    a[0]=a0; a[1]=a1; a[2]=a2; a[3]=a3; a[4]=a4; a[5]=a5; a[6]=a6;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 7i64);
};
"""
if "str_snprintf5" not in code:
    code = code.replace('pub func:str_snprintf6', func5 + '\n// Six-arg version\npub func:str_snprintf6')
if "str_snprintf7" not in code:
    code = code.replace('pub func:str_snprintf8', func7 + '\n// Eight-arg version\npub func:str_snprintf8')

with open('src/str/strfmt.npk', 'w') as f:
    f.write(code)

# 7. Add @ to string casts
files = ['src/proc/exec.npk', 'src/io/printf.npk', 'src/io/bio/tmpfile.npk']
for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            code = f.read()
        code = code.replace('(path_env_name)', '(@path_env_name)')
        code = code.replace('(default_path)', '(@default_path)')
        code = code.replace('(colon_space)', '(@colon_space)')
        code = code.replace('(mode_w_plus_b)', '(@mode_w_plus_b)')
        with open(filepath, 'w') as f:
            f.write(code)

print("All fixes applied!")
