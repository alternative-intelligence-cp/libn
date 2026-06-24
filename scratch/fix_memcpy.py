with open('src/mem/memcpy.npk', 'r') as f:
    text = f.read()

# Fix drop issue
text = text.replace("drop(mcpy(dst, src, num_bytes));", "int8->:_discard = mcpy(@cast_unchecked<int64>(dst), @cast_unchecked<int64>(src), num_bytes);")
text = text.replace("drop(mmov(dst, src, num_bytes));", "int8->:_discard = mmov(@cast_unchecked<int64>(dst), @cast_unchecked<int64>(src), num_bytes);")

# Update signatures to use any->
# pub func:mem_memcpy = int64(int64:dst, int64:src, int64:num_bytes)
text = text.replace("pub func:mem_memcpy = int64(int64:dst, int64:src, int64:num_bytes)", "pub func:mem_memcpy = any->(any->:dst, any->:src, int64:num_bytes)")

# mem_mempcpy
text = text.replace("pub func:mem_mempcpy = int64(int64:dst, int64:src, int64:num_bytes) {", "pub func:mem_mempcpy = any->(any->:dst, any->:src, int64:num_bytes) {")
text = text.replace("Result<int64>:r = mem_memcpy(dst, src, num_bytes);", "Result<any->>:r = mem_memcpy(dst, src, num_bytes);")
text = text.replace("pass dst + num_bytes;", "pass @cast_unchecked<any->>(@cast_unchecked<int64>(dst) + num_bytes);")

# mem_memmove
text = text.replace("pub func:mem_memmove = int64(int64:dst, int64:src, int64:num_bytes)", "pub func:mem_memmove = any->(any->:dst, any->:src, int64:num_bytes)")

# mem_memdup
text = text.replace("pub func:mem_memdup = int64(int64:src, int64:num_bytes) {", "pub func:mem_memdup = any->(any->:src, int64:num_bytes) {")
text = text.replace("Result<int64>:r = mem_malloc(num_bytes);", "Result<int64>:r = mem_malloc(num_bytes);")
text = text.replace("Result<int64>:rc = mem_memcpy(r.value, src, num_bytes);", "Result<any->>:rc = mem_memcpy(@cast_unchecked<any->>(r.value), src, num_bytes);")
text = text.replace("pass r.value;", "pass @cast_unchecked<any->>(r.value);")

# NULL checks
text = text.replace("dst != 0i64 && src != 0i64", "dst != NULL && src != NULL")
text = text.replace("src == 0i64", "src == NULL")

with open('src/mem/memcpy.npk', 'w') as f:
    f.write(text)

