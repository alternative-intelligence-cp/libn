import re
with open('src/str/strcpy.npk', 'r') as f:
    text = f.read()

# Fix Line 53 and other NULL comparisons
text = text.replace("dst == 0i64", "dst == @cast_unchecked<any->>(0i64)")
text = text.replace("src == 0i64", "src == @cast_unchecked<any->>(0i64)")

# Restore drop for mem_bzero
text = text.replace("mem_bzero(@cast_unchecked<int64>(dst), n);", "drop(mem_bzero(@cast_unchecked<int64>(dst), n));")
text = text.replace("mem_bzero(@cast_unchecked<int64>(dst) + nul_pos, dst_size - nul_pos);", "drop(mem_bzero(@cast_unchecked<int64>(dst) + nul_pos, dst_size - nul_pos));")

# Fix libn_slab_free / realloc calls
text = text.replace("libn_slab_free(r)", "libn_slab_free(@cast_unchecked<int64>(r))")

with open('src/str/strcpy.npk', 'w') as f:
    f.write(text)

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

# Actually we should just cast pointers passed to libn_slab_free
# But let's change libn_slab_free to accept any-> since pointers should be any->
text = text.replace("pub func:libn_slab_free = int64(int64:ptr)", "pub func:libn_slab_free = int64(any->:ptr)")
text = text.replace("if (ptr == 0i64) {", "if (ptr == @cast_unchecked<any->>(0i64)) {")
text = text.replace("int64:slot_start = ptr - SLAB_HEADER_SIZE;", "int64:slot_start = @cast_unchecked<int64>(ptr) - SLAB_HEADER_SIZE;")
text = text.replace("if ((ptr & 4095i64) == 16i64) {", "if ((@cast_unchecked<int64>(ptr) & 4095i64) == 16i64) {")
text = text.replace("Result<int64>:r = mem_free(ptr);", "Result<int64>:r = mem_free(@cast_unchecked<int64>(ptr));")
text = text.replace("int64->:next_ptr = @cast_unchecked<int64->>(ptr);", "int64->:next_ptr = @cast_unchecked<int64->>(ptr);")
text = text.replace("libn_slab_free(ptr)", "libn_slab_free(@cast_unchecked<any->>(ptr))")

text = text.replace("pub func:libn_slab_realloc = int64(int64:ptr, int64:n)", "pub func:libn_slab_realloc = int64(any->:ptr, int64:n)")
text = text.replace("if ((ptr & 4095i64) == 16i64) {", "if ((@cast_unchecked<int64>(ptr) & 4095i64) == 16i64) {")
text = text.replace("Result<int64>:r = mem_realloc(ptr, n);", "Result<int64>:r = mem_realloc(@cast_unchecked<int64>(ptr), n);")

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)
