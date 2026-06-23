import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# 1. Fix remaining while/if syntax
text = re.sub(r'if \(prot & PROT_EXEC\) != 0i64 \{', r'if ((prot & PROT_EXEC) != 0i64) {', text)
text = re.sub(r'if new_size <= 0i64 \{', r'if (new_size <= 0i64) {', text)
text = re.sub(r'if new_size < copy_n \{', r'if (new_size < copy_n) {', text)
text = re.sub(r'while si < copy_n \{', r'while (si < copy_n) {', text)
text = re.sub(r'if map_size <= 0i64 \{', r'if (map_size <= 0i64) {', text)

# 2. Fix remaining pointer casts
text = re.sub(r'\*int64:hdr = \(ptr - ALLOC_HEADER_SIZE\) as \*int64;', r'int64->:hdr = @cast_unchecked<int64->>(ptr - ALLOC_HEADER_SIZE);', text)

# 3. Change ALL Result<int64> return declarations in mmap.npk to int64
# because these are low-level allocators and callers expect 0 on failure.
text = re.sub(r'pub func:([A-Za-z0-9_]+)\s*=\s*Result<int64>\(', r'pub func:\1 = int64(', text)

# 4. Handle all the `pass r;` where `r` is `Result<int64>`.
# Functions that return pointers (mem_mmap_raw, mem_mremap_raw, mem_malloc, mem_realloc)
# should pass 0i64 on error. Functions that return status (mem_munmap_raw, mem_mprotect_raw)
# should probably pass 0 on success, <0 on error. BUT actually the original code just unwrapped
# the sys return value!
# Let's just safely unwrap them using `fail r.error` for the raw functions,
# but for the `mem_malloc` functions we use `pass 0i64`.

# Let's manually replace the libn_* wrappers:
text = text.replace('Result<int64>:r = libn_mmap(addr, length, prot, flags, fd, offset);\n    pass r;',
                    'Result<int64>:r = libn_mmap(addr, length, prot, flags, fd, offset);\n    if (r.is_error) { fail r.error; }\n    pass r.value;')
text = text.replace('Result<int64>:r = libn_munmap(addr, length);\n    pass r;',
                    'Result<int64>:r = libn_munmap(addr, length);\n    if (r.is_error) { fail r.error; }\n    pass r.value;')
text = text.replace('Result<int64>:r = libn_mprotect(addr, length, prot);\n    pass r;',
                    'Result<int64>:r = libn_mprotect(addr, length, prot);\n    if (r.is_error) { fail r.error; }\n    pass r.value;')
text = text.replace('Result<int64>:r = libn_mremap(old_addr, old_size, new_size, flags, new_addr);\n    pass r;',
                    'Result<int64>:r = libn_mremap(old_addr, old_size, new_size, flags, new_addr);\n    if (r.is_error) { fail r.error; }\n    pass r.value;')
text = text.replace('Result<int64>:r = libn_msync(addr, length, flags);\n    pass r;',
                    'Result<int64>:r = libn_msync(addr, length, flags);\n    if (r.is_error) { fail r.error; }\n    pass r.value;')

# Now mem_malloc:
text = text.replace('Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if r.is_error {\n        fail r.err;\n    }',
                    'Result<int64>:r = libn_mmap(0i64, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);\n    if (r.is_error) { pass 0i64; }')

# mem_calloc
text = text.replace('Result<int64>:r = mem_malloc(total_bytes);\n    pass r;',
                    'Result<int64>:r = mem_malloc(total_bytes);\n    if (r.is_error) { pass 0i64; }\n    pass r.value;') # Wait, mem_malloc returns int64 now! So r is int64!
# Let's fix mem_calloc manually:
text = text.replace('Result<int64>:r = mem_malloc(total_bytes);\n    pass r;',
                    'pass mem_malloc(total_bytes);')

# mem_realloc
text = text.replace('Result<int64>:new_r = mem_malloc(new_size);\n    if (new_r.is_error) {\n        pass 0i64;\n    }',
                    'int64:new_r = mem_malloc(new_size);\n    if (new_r == 0i64) {\n        pass 0i64;\n    }')
text = text.replace('int64:new_ptr = new_r.value;',
                    'int64:new_ptr = new_r;')

# mem_alloc_pages
text = text.replace('Result<int64>:r = libn_mmap(0i64, length, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | extra_flags, -1i64, 0i64);\n    pass r;',
                    'Result<int64>:r = libn_mmap(0i64, length, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | extra_flags, -1i64, 0i64);\n    if (r.is_error) { pass 0i64; }\n    pass r.value;')

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

