import os
import re

# 1. file.npk: Fix `pub fixed int64:(-1i64) = -1i64;`
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
code = code.replace('pub fixed int64:(-1i64) = -1i64;', 'pub fixed int64:FILE_EOF = -1i64;')
# Fix any missed sys_open arguments from open.npk?
# In file.npk, if we had any missing variables we fix them.
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

# 2. slab.npk: Fix head unwrapping
# If mem_slab_freelist_get somehow returns Result<int64>, we unwrap it
with open('src/mem/slab.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'int64:head = mem_slab_freelist_get(cls);',
    'Result<int64>:head_r = mem_slab_freelist_get(cls);\n    int64:head = 0i64; if (!head_r.is_error) { head = head_r.value; }'
)
code = code.replace(
    'head = mem_slab_freelist_get(cls);',
    'Result<int64>:head_r2 = mem_slab_freelist_get(cls);\n        if (!head_r2.is_error) { head = head_r2.value; }'
)
code = code.replace(
    'int64:sz   = slab_class_size(cls);',
    'Result<int64>:sz_r = slab_class_size(cls);\n    int64:sz = 0i64; if (!sz_r.is_error) { sz = sz_r.value; }'
)
code = code.replace(
    'int64:cls  = raw slab_class_for_size(n);',
    'Result<int64>:cls_r = slab_class_for_size(n);\n    int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; }'
)
code = code.replace(
    'int64:cls = @cast_unchecked<int64>(hdr[0]);',
    'Result<int64>:cls_r = @cast_unchecked<int64>(hdr[0]);\n    int64:cls = 0i64; if (!cls_r.is_error) { cls = cls_r.value; } else { cls = @cast_unchecked<int64>(hdr[0]); }'
)
# Fix 'raw mem_slab_freelist_get'
code = code.replace(
    'int64:old_head = raw mem_slab_freelist_get(cls);',
    'Result<int64>:old_head_r = mem_slab_freelist_get(cls);\n    int64:old_head = 0i64; if (!old_head_r.is_error) { old_head = old_head_r.value; }'
)
with open('src/mem/slab.npk', 'w') as f:
    f.write(code)

# 3. fstr.npk: 
with open('src/io/bio/fstr.npk', 'r') as f:
    code = f.read()
code = code.replace('Result<int64>:c_r2 = fputc(@cast_unchecked<int64>(p[i]), fp);', 'Result<int64>:c_r2 = fputc(@cast_unchecked<int64>(p[i]), fp);')
with open('src/io/bio/fstr.npk', 'w') as f:
    f.write(code)

# 4. stdfiles.npk: Unused result from NIL-returning function
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
# Wait, "Unused result from NIL-returning function" usually means you called a function that returns NIL (or Result<NIL>) and didn't use it.
# e.g., drop bio_ensure_std_init(); if it returns Result<NIL>
code = code.replace('drop bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init();')
code = code.replace('Result<NIL>:_nil_r = bio_ensure_std_init();\n    Result<NIL>:_nil_r = bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init();')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# 5. fprintf.npk: 
with open('src/io/bio/fprintf.npk', 'r') as f:
    code = f.read()
code = code.replace('drop bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init();')
with open('src/io/bio/fprintf.npk', 'w') as f:
    f.write(code)

# 6. file.npk: 
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
code = code.replace('drop bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init();')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

# 7. fchar.npk: 
with open('src/io/bio/fchar.npk', 'r') as f:
    code = f.read()
code = code.replace('drop bio_ensure_std_init();', 'Result<NIL>:_nil_r = bio_ensure_std_init();')
with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(code)

# 8. fopen.npk: 
with open('src/io/bio/fopen.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:parse_ok = bio_parse_mode', 'Result<int64>:parse_ok_r = bio_parse_mode')
code = code.replace('if (parse_ok == 0i64)', 'int64:parse_ok = 0i64; if (!parse_ok_r.is_error) { parse_ok = parse_ok_r.value; } if (parse_ok == 0i64)')
code = code.replace('int64:fp = bio_alloc_file();', 'Result<int64>:fp_r = bio_alloc_file(); int64:fp = 0i64; if (!fp_r.is_error) { fp = fp_r.value; }')
code = code.replace('int64:init_r = bio_ensure_std_init', 'Result<NIL>:init_r = bio_ensure_std_init')
code = code.replace('int64:r1 = sys3(', 'Result<int64>:r1 = sys3(')
code = code.replace('int64:r2 = sys3(', 'Result<int64>:r2 = sys3(')
code = code.replace('int64:r3 = sys3(', 'Result<int64>:r3 = sys3(')
with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(code)

# 9. fio.npk: 
with open('src/io/bio/fio.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:parse_ok = bio_parse_mode', 'Result<int64>:parse_ok_r = bio_parse_mode')
code = code.replace('if (parse_ok == 0i64)', 'int64:parse_ok = 0i64; if (!parse_ok_r.is_error) { parse_ok = parse_ok_r.value; } if (parse_ok == 0i64)')
code = code.replace('int64:fp = bio_alloc_file();', 'Result<int64>:fp_r = bio_alloc_file(); int64:fp = 0i64; if (!fp_r.is_error) { fp = fp_r.value; }')
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(code)

# 10. string arrays in strfmt.npk and file.npk
# Replace bitwise mismatch in bio_parse_mode in file.npk
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()
code = code.replace('has_zero_byte(w)', 'has_zero_byte(@cast_unchecked<int64>(w))')
code = code.replace('has_zero_byte', 'raw has_zero_byte')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied final_resolution.py")
