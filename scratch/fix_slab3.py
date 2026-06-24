import re

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

# Add imports
if 'use "../mem/memcpy.npk".*;' not in text:
    text = text.replace('use "../syscall/errno.npk".*;', 'use "../syscall/errno.npk".*;\nuse "../syscall/syscall.npk".*;\nuse "../mem/memcpy.npk".*;')

# Fix line 192 (or around there): slot_full
text = text.replace('int64:slot_full = slab_class_size(i) + SLAB_HEADER_SIZE;', 'int64:slot_full = (raw slab_class_size(i)) + SLAB_HEADER_SIZE;')

# Fix line 206: libn_mmap
text = text.replace('Result<int64>:r = libn_mmap(0i64, slab_size,', 'Result<int64>:r = libn_mmap(@cast_unchecked<any->>(0i64), slab_size,')

# Fix slab_free to libn_slab_free taking any->:ptr
text = text.replace('pub func:slab_free = int64(int64:ptr) {', 'pub func:libn_slab_free = int64(any->:ptr) {\n    int64:ptr_i64 = @cast_unchecked<int64>(ptr);\n')
# Now replace 'ptr' with 'ptr_i64' inside libn_slab_free ONLY
# We know libn_slab_free is between "pub func:libn_slab_free = int64(any->:ptr) {" and "};"
# Let's just do targeted replacements inside libn_slab_free body
text = text.replace('if (ptr == 0i64) {', 'if (ptr_i64 == 0i64) {')
text = text.replace('int64:slot_start = ptr - SLAB_HEADER_SIZE;', 'int64:slot_start = ptr_i64 - SLAB_HEADER_SIZE;')
text = text.replace('if ((ptr & 4095i64) == 16i64) {', 'if ((ptr_i64 & 4095i64) == 16i64) {')
text = text.replace('Result<int64>:r = mem_free(ptr);', 'Result<int64>:r = mem_free(ptr_i64);')
text = text.replace('int64->:next_ptr = @cast_unchecked<int64->>(ptr);', 'int64->:next_ptr = @cast_unchecked<int64->>(ptr_i64);')

# Also rename remaining slab_free to libn_slab_free
text = text.replace('drop(slab_free(ptr));', 'drop(libn_slab_free(@cast_unchecked<any->>(ptr)));')

# Fix mem_memcpy in slab_realloc
text = text.replace('mem_memcpy(new_ptr, ptr, copy_size)', 'mem_memcpy(@cast_unchecked<any->>(new_ptr), @cast_unchecked<any->>(ptr), copy_size)')

# Fix raw SLAB_SIZES and SLAB_SLOTS (if they were changed, which they weren't in git checkout, but let's make sure they are NOT changed to raw, since that breaks it)

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

