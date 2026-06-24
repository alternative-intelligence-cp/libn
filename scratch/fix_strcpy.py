with open('src/str/strcpy.npk', 'r') as f:
    text = f.read()

# Make sure we don't accidentally replace stuff we didn't mean to
replacements = [
    ("pub func:str_strcpy = int64(int64:dst, int64:src)", "pub func:str_strcpy = any->(any->:dst, any->:src)"),
    ("pub func:str_stpcpy = int64(int64:dst, int64:src)", "pub func:str_stpcpy = any->(any->:dst, any->:src)"),
    ("pub func:str_strncpy = int64(int64:dst, int64:src, int64:n)", "pub func:str_strncpy = any->(any->:dst, any->:src, int64:n)"),
    ("pub func:str_stpncpy = int64(int64:dst, int64:src, int64:n)", "pub func:str_stpncpy = any->(any->:dst, any->:src, int64:n)"),
    ("pub func:str_strdup = int64(int64:src)", "pub func:str_strdup = any->(any->:src)"),
    ("pub func:str_strndup = int64(int64:src, int64:n)", "pub func:str_strndup = any->(any->:src, int64:n)"),

    # Null checks
    ("if (dst == 0i64 || src == 0i64)", "if (dst == NULL || src == NULL)"),
    ("if (dst == 0i64 || n <= 0i64)", "if (dst == NULL || n <= 0i64)"),
    ("if (src == 0i64)", "if (src == NULL)"),

    # Returns
    ("pass dst + i;", "pass @cast_unchecked<any->>(@d[i]);"),
    ("int64:end_idx = dst + i;", "any->:end_idx = @cast_unchecked<any->>(@d[i]);"),

    # strdup memory allocation and copy
    ("int64:n = raw str_strlen(src);", "int64:n = raw str_strlen(src);"),
    ("int64:r = libn_slab_alloc(alloc_size);", "int64:r = libn_slab_alloc(alloc_size);"),
    ("drop(mem_memcpy(r, src, alloc_size));", "drop(mem_memcpy(r, @cast_unchecked<int64>(src), alloc_size));\n    any->:r_ptr = @cast_unchecked<any->>(r);"),
    ("pass r;", "pass r_ptr;"),

    # strndup memory allocation and copy
    ("drop(mem_memcpy(r, src, actual_len));", "drop(mem_memcpy(r, @cast_unchecked<int64>(src), actual_len));\n    any->:r_ptr = @cast_unchecked<any->>(r);"),
    ("(@cast_unchecked<uint8->>(r))[actual_len] = 0u8;", "(@cast_unchecked<uint8->>(r_ptr))[actual_len] = 0u8;"),

    # strncpy bzero
    ("drop(mem_bzero(dst, n));", "drop(mem_bzero(@cast_unchecked<int64>(dst), n));"),

    # str_strnlen call inside str_strndup
    ("int64:actual_len = raw str_strnlen(src, n);", "int64:actual_len = raw str_strnlen(src, n);")
]

for old, new in replacements:
    text = text.replace(old, new)

with open('src/str/strcpy.npk', 'w') as f:
    f.write(text)

