with open('src/mem/slab.npk', 'r') as f:
    content = f.read()

# 1. Update slab_refill loop to set canary
target1 = """        uint8->:hdr_byte = @cast_unchecked<uint8->>(slot_start);
        hdr_byte[0] = @cast_unchecked<uint8>(i);    // class index in header uint8"""
replacement1 = """        uint8->:hdr_byte = @cast_unchecked<uint8->>(slot_start);
        hdr_byte[0] = @cast_unchecked<uint8>(i);    // class index in header uint8
        hdr_byte[1] = 0xDFu8;                       // 0xDF = free canary"""
content = content.replace(target1, replacement1)

# 2. Update slab_alloc to set allocated canary
target2 = """      // Clear the "next" pointer field before handing to user
      // (The slot was zero-initialized by mmap on first use; on reuse, clear it)
    next_ptr[0] = 0i64;

    pass user_ptr;"""
replacement2 = """      // Clear the "next" pointer field before handing to user
      // (The slot was zero-initialized by mmap on first use; on reuse, clear it)
    next_ptr[0] = 0i64;
    
    uint8->:alloc_hdr = @cast_unchecked<uint8->>(head);
    alloc_hdr[1] = 0xAAu8; // 0xAA = allocated canary

    pass user_ptr;"""
content = content.replace(target2, replacement2)

# 3. Update slab_free to check double-free
target3 = """    if ((ptr & 4095i64) == 16i64) {
          // @cast_unchecked<direct>(Treat)-mmap allocation — use mem_free with the actual ptr.
          // The direct-mmap header is 16 bytes before the user pointer.
        Result<int64>:r = mem_free(ptr);
        return r;
    }

      // Push slot back onto freelist:"""
replacement3 = """    if ((ptr & 4095i64) == 16i64) {
          // @cast_unchecked<direct>(Treat)-mmap allocation — use mem_free with the actual ptr.
          // The direct-mmap header is 16 bytes before the user pointer.
        Result<int64>:r = mem_free(ptr);
        return r;
    }
    
    if (hdr[1] == 0xDFu8) {
        // Double free detected!
        fail @cast_unchecked<tbb32>(ERR_INTERNAL);
    }
    hdr[1] = 0xDFu8; // set to free canary

      // Push slot back onto freelist:"""
content = content.replace(target3, replacement3)

with open('src/mem/slab.npk', 'w') as f:
    f.write(content)
