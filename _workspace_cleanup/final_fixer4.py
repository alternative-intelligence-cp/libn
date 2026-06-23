import os

with open('src/syscall/syscall.npk', 'r') as f:
    code = f.read()
# Replace sys_safe body
sys_safe_old = """    int64:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (ret > -4096i64 && ret < 0i64) {
        fail @cast_unchecked<int64>(0i64 - ret);
    }
    pass raw ret;"""
sys_safe_new = """    Result<int64>:r_sys = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (r_sys.is_error) {
        fail r_sys.error;
    }
    pass r_sys.value;"""
code = code.replace(sys_safe_old, sys_safe_new)
with open('src/syscall/syscall.npk', 'w') as f:
    f.write(code)

with open('src/mem/memutil.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'diff = diff | (@cast_unchecked<int64>(@cast_unchecked<int64>(pa[i]) ^ pb[i]));',
    'diff = diff | (@cast_unchecked<int64>(pa[i]) ^ @cast_unchecked<int64>(pb[i]));'
)
code = code.replace(
    'int64:tword = raw replicate_byte(c);',
    'int64:tword = raw replicate_byte(@cast_unchecked<uint8>(c));'
)
code = code.replace(
    '// Match is somewhere in this word — find exact uint8 int64:word_base = ptr + i + wi * 8i64;',
    '// Match is somewhere in this word — find exact uint8\n            int64:word_base = ptr + i + wi * 8i64;'
)
with open('src/mem/memutil.npk', 'w') as f:
    f.write(code)

print("Applied final_fixer4.py")
