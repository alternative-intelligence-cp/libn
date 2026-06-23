import os
import re

def rewrite(path, func):
    with open(path, 'r') as f:
        code = f.read()
    new_code = func(code)
    if code != new_code:
        with open(path, 'w') as f:
            f.write(new_code)
        print(f"Fixed {path}")

# 1. Rename slab_free to mem_slab_free
def rename_slab_free(code):
    return re.sub(r'\bslab_free\b', 'mem_slab_free', code)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            rewrite(os.path.join(root, file), rename_slab_free)

# 2. Fix stdfiles.npk @g_stdin_file
def fix_stdfiles(code):
    code = code.replace('@cast_unchecked<FILE->>(g_stdin_file)', '@cast_unchecked<FILE->>(@g_stdin_file)')
    code = code.replace('@cast_unchecked<FILE->>(g_stdout_file)', '@cast_unchecked<FILE->>(@g_stdout_file)')
    code = code.replace('@cast_unchecked<FILE->>(g_stderr_file)', '@cast_unchecked<FILE->>(@g_stderr_file)')
    code = code.replace('@cast_unchecked<int64>(g_stdin_file)', '@cast_unchecked<int64>(@g_stdin_file)')
    code = code.replace('@cast_unchecked<int64>(g_stdout_file)', '@cast_unchecked<int64>(@g_stdout_file)')
    code = code.replace('@cast_unchecked<int64>(g_stderr_file)', '@cast_unchecked<int64>(@g_stderr_file)')
    return code

rewrite('src/io/bio/stdfiles.npk', fix_stdfiles)

# 3. Fix strfmt.npk
def fix_strfmt(code):
    # Fix comment corruption
    code = code.replace('@cast_unchecked<the>("9223372036854775807")', 'as the "9223372036854775807"')
    
    # Append missing functions
    if 'str_snprintf5' not in code:
        code += """
pub func:str_snprintf5 = int64(int64:buf, int64:buf_size, int64:fmt, int64:a0, int64:a1, int64:a2, int64:a3, int64:a4) {
    stack int64[5]:a;
    a[0] = a0; a[1] = a1; a[2] = a2; a[3] = a3; a[4] = a4;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 5i64);
};

pub func:str_snprintf7 = int64(int64:buf, int64:buf_size, int64:fmt, int64:a0, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {
    stack int64[7]:a;
    a[0] = a0; a[1] = a1; a[2] = a2; a[3] = a3; a[4] = a4; a[5] = a5; a[6] = a6;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 7i64);
};
"""
    return code
rewrite('src/str/strfmt.npk', fix_strfmt)

# 4. Fix strlen.npk has_nul_byte -> has_zero_byte and !v -> (~v)
def fix_strlen(code):
    code = code.replace('has_nul_byte', 'has_zero_byte')
    code = code.replace('!v', '(~v)')
    return code
rewrite('src/str/strlen.npk', fix_strlen)

# 5. Fix memutil.npk !v -> (~v)
def fix_memutil(code):
    code = code.replace('!v', '(~v)')
    return code
rewrite('src/mem/memutil.npk', fix_memutil)

