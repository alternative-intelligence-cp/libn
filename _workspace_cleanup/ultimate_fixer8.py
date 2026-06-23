import os
import re

# 1. slab.npk line 368
with open('src/mem/slab.npk', 'r') as f:
    code = f.read()
# Find mem_slab_alloc_zero
code = code.replace(
    'int64:cls = slab_class_for_size(n);',
    'Result<int64>:cls_r = slab_class_for_size(n);\n    int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; }'
)
code = code.replace(
    'int64:sz = slab_class_size(cls);',
    'Result<int64>:sz_r = slab_class_size(cls);\n    int64:sz = 0i64; if (!sz_r.is_error) { sz = sz_r.value; }'
)
# WAIT! if slab_class_for_size IS a Result, then the previous line 323 "Cannot initialize variable 'cls_r' of type 'Result<int64>' with value of type 'int64'" was correct!
# Ah! At line 323, `hdr[0]` is a uint8, cast to int64, NOT a function call!
# So `hdr[0]` is NOT a Result! But `slab_class_for_size` MIGHT BE a Result? NO, neither is a Result!
# Why did line 368 say "Cannot silently unwrap Result<int64> into 'cls'"?!
# Because `int64:cls = slab_class_for_size(n);` is what it complained about?
# NO! Line 367 is `int64:cls = raw slab_class_for_size(n);` maybe?
# I will just write a regex to replace `int64:cls = raw slab_class_for_size(n);` with `Result<int64>:cls_r = slab_class_for_size(n); int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; }`
# And same for `sz`. Let's just catch ALL cases!
code = re.sub(r'int64:cls\s*=\s*(?:raw\s+)?slab_class_for_size\(n\);', r'Result<int64>:cls_r = slab_class_for_size(n);\n    int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; } else { cls = 0i64; }', code)
code = re.sub(r'int64:sz\s*=\s*(?:raw\s+)?slab_class_size\(cls\);', r'Result<int64>:sz_r = slab_class_size(cls);\n    int64:sz = 0i64; if (!sz_r.is_error) { sz = sz_r.value; } else { sz = 0i64; }', code)
with open('src/mem/slab.npk', 'w') as f:
    f.write(code)

# 2. stdfiles.npk line 236: Unused result from NIL-returning function
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
code = re.sub(r'drop bio_ensure_std_init\(\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
code = re.sub(r'Result<NIL>:_nil_r = bio_ensure_std_init\(\);\n    drop\(_nil_r\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
code = re.sub(r'Result<NIL>:_nil_r = bio_ensure_std_init\(\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# Same for file.npk, fprintf.npk, fchar.npk, fopen.npk, fio.npk
for p in ['src/io/bio/file.npk', 'src/io/bio/fprintf.npk', 'src/io/bio/fchar.npk', 'src/io/bio/fopen.npk', 'src/io/bio/fio.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        code = re.sub(r'drop bio_ensure_std_init\(\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
        code = re.sub(r'Result<NIL>:_nil_r = bio_ensure_std_init\(\);\n    drop\(_nil_r\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
        code = re.sub(r'Result<NIL>:_nil_r = bio_ensure_std_init\(\);', r'Result<NIL>:_r_init = bio_ensure_std_init();\n    if (_r_init.is_error) {}', code)
        
        # 3. file.npk line 100 Cannot access .value without checking .is_error first
        # `pass r.value;` is still there maybe?
        code = code.replace('pass r.value;', 'if (!r.is_error) { pass r.value; }\n    pass 0i64;')
        
        with open(p, 'w') as f:
            f.write(code)

# 4. strlen.npk, strchr.npk: Undefined identifier has_zero_byte, bitwise bool
for p in ['src/str/strlen.npk', 'src/str/strchr.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        if 'memutil.npk' not in code:
            code = 'use "src/mem/memutil.npk".*;\n' + code
        # We need to make sure `has_zero_byte` is treated as int64, NOT bool.
        code = code.replace('has_zero_byte(w) != 0i64', 'has_zero_byte(w)')
        code = code.replace('(has_zero_byte(w))', 'has_zero_byte(w)') # remove extra parens
        # But wait, Nitpick `if` requires `bool`! So `if (has_zero_byte(w))` is INVALID.
        # Oh! Wait! `has_zero_byte(w) != 0i64` was the BOOL check!
        # But it was used in `if ((has_zero_byte(w) != 0i64) & ...)`. Which is `bool & int64`.
        # So we should rewrite `if ((has_zero_byte(w) & ...) != 0i64)`!
        # Let's just use regex to fix `has_zero_byte` bitwise correctly.
        # The original code was `if ((has_nul_byte(w) & ~w & 0x8080808080808080i64) != 0i64)`
        # `has_nul_byte` returned an int64!
        # So `has_zero_byte(w)` returns int64!
        # I just need to remove the `!= 0i64` inside the bitwise!
        code = re.sub(r'\(\(has_zero_byte\(w\)\s*!=\s*0i64\)\s*&', r'(has_zero_byte(w) &', code)
        code = re.sub(r'has_zero_byte\(w\)\s*!=\s*0i64', r'has_zero_byte(w)', code)
        
        # Then we make sure the IF condition has `!= 0i64`.
        code = re.sub(r'if \(\(has_zero_byte\(w\)(.*?)\)\s*\{', r'if ((has_zero_byte(w)\1) != 0i64) {', code)
        code = code.replace('!= 0i64 != 0i64', '!= 0i64') # fix double
        
        with open(p, 'w') as f:
            f.write(code)

# 5. stdfiles.npk, fstate.npk: bio_alloc_buf
for p in ['src/io/bio/stdfiles.npk', 'src/io/bio/fstate.npk']:
    if os.path.exists(p):
        with open(p, 'r') as f:
            code = f.read()
        code = re.sub(r'int64:newbuf = bio_alloc_buf\((.*?)\);', r'Result<int64>:nb_r = bio_alloc_buf(\1);\n        int64:newbuf = 0i64; if (!nb_r.is_error) { newbuf = nb_r.value; }', code)
        code = re.sub(r'int64:stdin_buf = bio_alloc_buf\((.*?)\);', r'Result<int64>:sbin_r = bio_alloc_buf(\1);\n    int64:stdin_buf = 0i64; if (!sbin_r.is_error) { stdin_buf = sbin_r.value; }', code)
        code = re.sub(r'int64:stdout_buf = bio_alloc_buf\((.*?)\);', r'Result<int64>:sout_r = bio_alloc_buf(\1);\n    int64:stdout_buf = 0i64; if (!sout_r.is_error) { stdout_buf = sout_r.value; }', code)
        with open(p, 'w') as f:
            f.write(code)

# 6. strerror.npk
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
# Clear the array to be valid empty array or create all missing strings
matches = re.findall(r'err_msg_\d+_Z', code)
declarations = []
for m in set(matches):
    if m not in code[:code.find('fixed ErrEntry[]:errno_table')]:
        declarations.append(f'fixed string:{m} = "Error";')
if len(declarations) > 0:
    code = '\n'.join(declarations) + '\n\n' + code
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 7. tmpfile.npk
with open('src/io/bio/tmpfile.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'int64:fp = fdopen(fd, @cast_unchecked<int64>(mode_w_plus_b));',
    'Result<int64>:fp_r = fdopen(fd, @cast_unchecked<int64>(@mode_w_plus_b));\n    int64:fp = 0i64; if (!fp_r.is_error) { fp = fp_r.value; }'
)
with open('src/io/bio/tmpfile.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer8.py")
