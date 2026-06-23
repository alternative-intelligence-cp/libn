import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# 1. Fix closing braces
text = re.sub(r'^\}\n', '};\n', text, flags=re.MULTILINE)

# 2. Fix if/while statements
text = re.sub(r'if length <= 0i64 \{', 'if (length <= 0i64) {', text)
text = re.sub(r'if n <= 0i64 \{', 'if (n <= 0i64) {', text)
text = re.sub(r'if r\.is_error \{', 'if (r.is_error) {', text)
text = re.sub(r'if !r\.is_error \{', 'if (!r.is_error) {', text)
text = re.sub(r'if ptr == 0i64 \{', 'if (ptr == 0i64) {', text)
text = re.sub(r'if new_size == 0i64 \{', 'if (new_size == 0i64) {', text)
text = re.sub(r'if new_r\.is_error \{', 'if (new_r.is_error) {', text)
text = re.sub(r'if !rr\.is_error \{', 'if (!rr.is_error) {', text)
text = re.sub(r'if size > 0i64 && n > \(9223372036854775807i64 / size\) \{', 'if (size > 0i64 && n > (9223372036854775807i64 / size)) {', text)
text = re.sub(r'if n <= 0i64 \|\| size <= 0i64 \{', 'if (n <= 0i64 || size <= 0i64) {', text)
text = re.sub(r'if \(prot & PROT_EXEC\) != 0i64 \{', 'if ((prot & PROT_EXEC) != 0i64) {', text)
text = re.sub(r'if new_size <= 0i64 \{', 'if (new_size <= 0i64) {', text)
text = re.sub(r'if new_size < copy_n \{', 'if (new_size < copy_n) {', text)
text = re.sub(r'while si < copy_n \{', 'while (si < copy_n) {', text)
text = re.sub(r'if map_size <= 0i64 \{', 'if (map_size <= 0i64) {', text)
text = re.sub(r'if n_pages <= 0i64 \{', 'if (n_pages <= 0i64) {', text)
text = re.sub(r'if n_pages <= 0i64 \|\| addr == 0i64 \{', 'if (n_pages <= 0i64 || addr == 0i64) {', text)
text = re.sub(r'if n_data_pages <= 0i64 \{', 'if (n_data_pages <= 0i64) {', text)
text = re.sub(r'if r_bot\.is_error \{', 'if (r_bot.is_error) {', text)
text = re.sub(r'if r_top\.is_error \{', 'if (r_top.is_error) {', text)
text = re.sub(r'if data_ptr == 0i64 \|\| n_data_pages <= 0i64 \{', 'if (data_ptr == 0i64 || n_data_pages <= 0i64) {', text)

# 3. Fix pointer casts
text = re.sub(r'\*int64:hdr = map_start as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(map_start);', text)
text = re.sub(r'\*int64:new_hdr = new_map as \*int64;', 'int64->:new_hdr = @cast_unchecked<int64->>(new_map);', text)
text = re.sub(r'\*int64:hdr = ptr as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(ptr);', text)
text = re.sub(r'\*byte:src = ptr as \*byte;', 'uint8->:src = @cast_unchecked<uint8->>(ptr);', text)
text = re.sub(r'\*byte:dst = new_ptr as \*byte;', 'uint8->:dst = @cast_unchecked<uint8->>(new_ptr);', text)
text = re.sub(r'\*int64:hdr = \(ptr - ALLOC_HEADER_SIZE\) as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(ptr - ALLOC_HEADER_SIZE);', text)

# 4. Fix fail errors
text = re.sub(r'fail ERR_BADARG as tbb8;', 'fail ERR_BADARG;', text)
text = re.sub(r'fail ERR_OVERFLOW as tbb8;', 'fail ERR_OVERFLOW;', text)
text = re.sub(r'\.err;', '.error;', text)

# 5. Fix implicit pass Result bug
text = re.sub(r'Result<int64>:r = libn_mmap\(([^)]+)\);\s*pass r;', r'Result<int64>:r = libn_mmap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_munmap\(([^)]+)\);\s*pass r;', r'Result<int64>:r = libn_munmap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_mprotect\(([^)]+)\);\s*pass r;', r'Result<int64>:r = libn_mprotect(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_mremap\(([^)]+)\);\s*pass r;', r'Result<int64>:r = libn_mremap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_msync\(([^)]+)\);\s*pass r;', r'Result<int64>:r = libn_msync(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)

# mem_malloc explicit unwrap
text = text.replace('Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if (r.is_error) {\n        fail r.error;\n    }\n\n    // Write header at map start.\n    int64:map_start = r.value;',
                    'Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if (r.is_error) { fail r.error; }\n    int64:map_start = r.value;')

# mem_realloc fixes
text = text.replace('int64:new_ptr = new_r;', 'int64:new_ptr = new_r.value;')

# 6. Fix compiler bug for page_align_up function calls
text = re.sub(r'page_align_up\(', r'raw page_align_up(', text)

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
