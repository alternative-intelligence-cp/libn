import re

with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# 1. Revert Explicit Result<int64> declarations back to int64()
text = re.sub(r'pub func:([A-Za-z0-9_]+) = Result<int64>\(', r'pub func:\1 = int64(', text)

# 2. Fix pass r; inside those functions to manually unwrap
text = re.sub(r'Result<int64>:r = libn_mmap\(([^)]+)\);\n\s*pass r;', r'Result<int64>:r = libn_mmap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_munmap\(([^)]+)\);\n\s*pass r;', r'Result<int64>:r = libn_munmap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_mprotect\(([^)]+)\);\n\s*pass r;', r'Result<int64>:r = libn_mprotect(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_mremap\(([^)]+)\);\n\s*pass r;', r'Result<int64>:r = libn_mremap(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)
text = re.sub(r'Result<int64>:r = libn_msync\(([^)]+)\);\n\s*pass r;', r'Result<int64>:r = libn_msync(\1);\n    if (r.is_error) { fail r.error; }\n    pass r.value;', text)

# 3. Add raw to page_align_up function calls
text = re.sub(r'page_align_up\(', r'raw page_align_up(', text)

# 4. Fix implicit Result wrapping for mem_malloc inside mem_calloc
text = text.replace('Result<int64>:r = mem_malloc(total);\n    int64:ptr = r;', 'Result<int64>:r = mem_malloc(total);\n    if (r.is_error) { fail r.error; }\n    int64:ptr = r.value;')

# 5. Fix implicit Result wrapping for mem_malloc inside mem_realloc
text = text.replace('Result<int64>:new_r = mem_malloc(new_size);\n        if new_r.is_error {\n            fail new_r.err;\n        }\n        int64:new_ptr = new_r;', 'Result<int64>:new_r = mem_malloc(new_size);\n        if (new_r.is_error) {\n            fail new_r.error;\n        }\n        int64:new_ptr = new_r.value;')

# 6. mem_malloc specific fixes
text = text.replace('Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if r.is_error {\n        fail r.err;\n    }\n\n    // Write header at map start.\n    int64:map_start = r;',
                    'Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if (r.is_error) { fail r.error; }\n\n    // Write header at map start.\n    int64:map_start = r.value;')

# 7. if statements without parens
text = re.sub(r'if ([A-Za-z0-9_]+)\.is_error \{', r'if (\1.is_error) {', text)
text = re.sub(r'if length <= 0i64 \{', 'if (length <= 0i64) {', text)
text = re.sub(r'if n <= 0i64 \{', 'if (n <= 0i64) {', text)
text = re.sub(r'if new_size == 0i64 \{', 'if (new_size == 0i64) {', text)
text = re.sub(r'if ptr == 0i64 \{', 'if (ptr == 0i64) {', text)
text = re.sub(r'if size > 0i64 && n > \(9223372036854775807i64 / size\) \{', 'if (size > 0i64 && n > (9223372036854775807i64 / size)) {', text)
text = re.sub(r'if n <= 0i64 \|\| size <= 0i64 \{', 'if (n <= 0i64 || size <= 0i64) {', text)
text = re.sub(r'if new_size <= 0i64 \{', 'if (new_size <= 0i64) {', text)
text = re.sub(r'if new_size < copy_n \{', 'if (new_size < copy_n) {', text)
text = re.sub(r'while si < copy_n \{', 'while (si < copy_n) {', text)
text = re.sub(r'if map_size <= 0i64 \{', 'if (map_size <= 0i64) {', text)
text = re.sub(r'if n_pages <= 0i64 \{', 'if (n_pages <= 0i64) {', text)
text = re.sub(r'if n_pages <= 0i64 \|\| addr == 0i64 \{', 'if (n_pages <= 0i64 || addr == 0i64) {', text)
text = re.sub(r'if n_data_pages <= 0i64 \{', 'if (n_data_pages <= 0i64) {', text)
text = re.sub(r'if data_ptr == 0i64 \|\| n_data_pages <= 0i64 \{', 'if (data_ptr == 0i64 || n_data_pages <= 0i64) {', text)
text = re.sub(r'if \(prot & PROT_EXEC\) != 0i64 \{', 'if ((prot & PROT_EXEC) != 0i64) {', text)
text = re.sub(r'if !r.is_error \{', 'if (!r.is_error) {', text)
text = re.sub(r'if !rr.is_error \{', 'if (!rr.is_error) {', text)

# 8. Pointer casts
text = re.sub(r'\*int64:hdr = map_start as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(map_start);', text)
text = re.sub(r'\*int64:new_hdr = new_map as \*int64;', 'int64->:new_hdr = @cast_unchecked<int64->>(new_map);', text)
text = re.sub(r'\*int64:hdr = ptr as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(ptr);', text)
text = re.sub(r'\*byte:src = ptr as \*byte;', 'uint8->:src = @cast_unchecked<uint8->>(ptr);', text)
text = re.sub(r'\*byte:dst = new_ptr as \*byte;', 'uint8->:dst = @cast_unchecked<uint8->>(new_ptr);', text)
text = re.sub(r'\*int64:hdr = \(ptr - ALLOC_HEADER_SIZE\) as \*int64;', 'int64->:hdr = @cast_unchecked<int64->>(ptr - ALLOC_HEADER_SIZE);', text)

# 9. Enums / constants casts
text = re.sub(r'fail ERR_BADARG as tbb8;', 'fail ERR_BADARG;', text)
text = re.sub(r'fail ERR_OVERFLOW as tbb8;', 'fail ERR_OVERFLOW;', text)
text = re.sub(r'\.err;', '.error;', text)

# Clean up raw raw
text = re.sub(r'raw raw ', 'raw ', text)

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
