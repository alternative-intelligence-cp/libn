with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

text = text.replace("NULL", "@cast_unchecked<any->>(0i64)")
text = text.replace("libn_slab_free(ptr)", "libn_slab_free(@cast_unchecked<int64>(ptr))")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

# Fix libn_mmap(0i64, ...)
text = text.replace("libn_mmap(0i64,", "libn_mmap(@cast_unchecked<any->>(0i64),")

# Fix mem_memcpy in slab_realloc
text = text.replace("drop(mem_memcpy(new_ptr, ptr, copy_size));", "Result<any->>:_rc = mem_memcpy(@cast_unchecked<any->>(new_ptr), @cast_unchecked<any->>(ptr), copy_size);")

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)
