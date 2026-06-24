import re

with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# Replace libn_mmap(addr...) with libn_mmap(@cast_unchecked<any->>(addr)...)
text = text.replace("libn_mmap(addr,", "libn_mmap(@cast_unchecked<any->>(addr),")
text = text.replace("libn_munmap(addr,", "libn_munmap(@cast_unchecked<any->>(addr),")
text = text.replace("libn_mprotect(addr,", "libn_mprotect(@cast_unchecked<any->>(addr),")
text = text.replace("libn_mremap(old_addr,", "libn_mremap(@cast_unchecked<any->>(old_addr),")
text = text.replace("libn_madvise(addr,", "libn_madvise(@cast_unchecked<any->>(addr),")
text = text.replace("libn_msync(addr,", "libn_msync(@cast_unchecked<any->>(addr),")

# Replace libn_mmap(NULL...)
text = text.replace("libn_mmap(NULL,", "libn_mmap(@cast_unchecked<any->>(0i64),")

# Add casting for MREMAP_MAYMOVE's last arg
text = text.replace("MREMAP_MAYMOVE, new_addr)", "MREMAP_MAYMOVE, @cast_unchecked<any->>(new_addr))")
text = text.replace("MREMAP_MAYMOVE, 0i64)", "MREMAP_MAYMOVE, @cast_unchecked<any->>(0i64))")

# Add casting for base, map_start, top_guard
text = text.replace("libn_munmap(map_start,", "libn_munmap(@cast_unchecked<any->>(map_start),")
text = text.replace("libn_munmap(base,", "libn_munmap(@cast_unchecked<any->>(base),")
text = text.replace("libn_mprotect(base,", "libn_mprotect(@cast_unchecked<any->>(base),")
text = text.replace("libn_mprotect(top_guard,", "libn_mprotect(@cast_unchecked<any->>(top_guard),")

text = text.replace("libn_mremap(map_start,", "libn_mremap(@cast_unchecked<any->>(map_start),")

# Replace slab_free(ptr)
text = text.replace("slab_free(ptr)", "libn_slab_free(@cast_unchecked<int64>(ptr))")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

