with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# Fix NULL in libn_mmap
text = text.replace("libn_mmap(NULL", "libn_mmap(@cast_unchecked<any->>(0i64)")

# Fix libn_mremap new_addr
text = text.replace("libn_mremap(@cast_unchecked<any->>(old_addr), old_size, new_size, flags, new_addr)", "libn_mremap(@cast_unchecked<any->>(old_addr), old_size, new_size, flags, @cast_unchecked<any->>(new_addr))")

# Fix libn_slab_free back to slab_free
text = text.replace("libn_slab_free(@cast_unchecked<int64>(ptr))", "slab_free(ptr)")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
