with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# Fix libn_* inline casts by pre-casting
text = text.replace("Result<int64>:r = libn_mmap(@cast_unchecked<any->>(addr), length, prot, flags, fd, offset);", 
                    "any->:addr_ptr = @cast_unchecked<any->>(addr);\n    Result<int64>:r = libn_mmap(addr_ptr, length, prot, flags, fd, offset);")

text = text.replace("Result<int64>:r = libn_munmap(@cast_unchecked<any->>(addr), length);",
                    "any->:addr_ptr = @cast_unchecked<any->>(addr);\n    Result<int64>:r = libn_munmap(addr_ptr, length);")

text = text.replace("Result<int64>:r = libn_mprotect(@cast_unchecked<any->>(addr), length, prot);",
                    "any->:addr_ptr = @cast_unchecked<any->>(addr);\n    Result<int64>:r = libn_mprotect(addr_ptr, length, prot);")

text = text.replace("Result<int64>:r = libn_mremap(@cast_unchecked<any->>(old_addr), old_size, new_size, flags, new_addr);",
                    "any->:old_addr_ptr = @cast_unchecked<any->>(old_addr);\n    any->:new_addr_ptr = @cast_unchecked<any->>(new_addr);\n    Result<int64>:r = libn_mremap(old_addr_ptr, old_size, new_size, flags, new_addr_ptr);")

text = text.replace("Result<int64>:r = libn_madvise(@cast_unchecked<any->>(addr), length, advice);",
                    "any->:addr_ptr = @cast_unchecked<any->>(addr);\n    Result<int64>:r = libn_madvise(addr_ptr, length, advice);")

text = text.replace("Result<int64>:r = libn_msync(@cast_unchecked<any->>(addr), length, flags);",
                    "any->:addr_ptr = @cast_unchecked<any->>(addr);\n    Result<int64>:r = libn_msync(addr_ptr, length, flags);")

# Fix NULL in libn_mmap
text = text.replace("Result<int64>:r = libn_mmap(NULL, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);",
                    "any->:null_ptr = @cast_unchecked<any->>(0i64);\n    Result<int64>:r = libn_mmap(null_ptr, total, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);")
text = text.replace("Result<int64>:r = libn_mmap(NULL, size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);",
                    "any->:null_ptr = @cast_unchecked<any->>(0i64);\n    Result<int64>:r = libn_mmap(null_ptr, size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);")
text = text.replace("Result<int64>:r = libn_mmap(NULL, total_size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);",
                    "any->:null_ptr = @cast_unchecked<any->>(0i64);\n    Result<int64>:r = libn_mmap(null_ptr, total_size, PROT_RW, MAP_ANON_PRIV, -1i64, 0i64);")

# Fix drop(libn_munmap...)
text = text.replace("drop(libn_munmap(@cast_unchecked<any->>(base), total_size));",
                    "any->:base_ptr = @cast_unchecked<any->>(base);\n        drop(libn_munmap(base_ptr, total_size));")
text = text.replace("Result<int64>:r_bot = libn_mprotect(@cast_unchecked<any->>(base), PAGE_SIZE, PROT_NONE);",
                    "any->:base_ptr = @cast_unchecked<any->>(base);\n    Result<int64>:r_bot = libn_mprotect(base_ptr, PAGE_SIZE, PROT_NONE);")
text = text.replace("Result<int64>:r_top = libn_mprotect(@cast_unchecked<any->>(top_guard), PAGE_SIZE, PROT_NONE);",
                    "any->:top_guard_ptr = @cast_unchecked<any->>(top_guard);\n    Result<int64>:r_top = libn_mprotect(top_guard_ptr, PAGE_SIZE, PROT_NONE);")

text = text.replace("Result<int64>:r = libn_munmap(@cast_unchecked<any->>(map_start), map_size);",
                    "any->:map_start_ptr = @cast_unchecked<any->>(map_start);\n    Result<int64>:r = libn_munmap(map_start_ptr, map_size);")
text = text.replace("Result<int64>:rr = libn_mremap(@cast_unchecked<any->>(map_start), old_map_size, new_total, MREMAP_MAYMOVE, 0i64);",
                    "any->:map_start_ptr = @cast_unchecked<any->>(map_start);\n    any->:null_ptr2 = @cast_unchecked<any->>(0i64);\n    Result<int64>:rr = libn_mremap(map_start_ptr, old_map_size, new_total, MREMAP_MAYMOVE, null_ptr2);")

# raw page_align_up
text = text.replace("int64:total = page_align_up(ALLOC_HEADER_SIZE + n);", "int64:total = raw page_align_up(ALLOC_HEADER_SIZE + n);")
text = text.replace("int64:new_total = page_align_up(ALLOC_HEADER_SIZE + new_size);", "int64:new_total = raw page_align_up(ALLOC_HEADER_SIZE + new_size);")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
