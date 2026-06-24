with open('src/str/strcpy.npk', 'r') as f:
    text = f.read()

replacements = [
    ("pub func:str_strcpy = int64(int64:dst, int64:src)", "pub func:str_strcpy = any->(any->:dst, any->:src)"),
    ("pub func:str_stpcpy = int64(int64:dst, int64:src)", "pub func:str_stpcpy = any->(any->:dst, any->:src)"),
    ("pub func:str_strncpy = int64(int64:dst, int64:src, int64:n)", "pub func:str_strncpy = any->(any->:dst, any->:src, int64:n)"),
    ("pub func:str_stpncpy = int64(int64:dst, int64:src, int64:n)", "pub func:str_stpncpy = any->(any->:dst, any->:src, int64:n)"),
    ("pub func:str_strdup = int64(int64:src)", "pub func:str_strdup = any->(any->:src)"),
    ("pub func:str_strndup = int64(int64:src, int64:n)", "pub func:str_strndup = any->(any->:src, int64:n)"),

    # drop issues with NIL functions
    ("drop(mem_bzero(dst, n));", "mem_bzero(@cast_unchecked<int64>(dst), n);"),
    ("drop(mem_bzero(dst + nul_pos, dst_size - nul_pos));", "mem_bzero(@cast_unchecked<int64>(dst) + nul_pos, dst_size - nul_pos);"),

    # Null checks
    ("if (dst == 0i64 || src == 0i64)", "if (dst == @cast_unchecked<any->>(0i64) || src == @cast_unchecked<any->>(0i64))"),
    ("if (dst == 0i64 || n <= 0i64)", "if (dst == @cast_unchecked<any->>(0i64) || n <= 0i64)"),
    ("if (src == 0i64)", "if (src == @cast_unchecked<any->>(0i64))"),

    # Returns
    ("pass dst + i;", "pass @cast_unchecked<any->>(@cast_unchecked<int64>(dst) + i);"),
    ("int64:end_idx = dst + i;", "any->:end_idx = @cast_unchecked<any->>(@cast_unchecked<int64>(dst) + i);"),
    ("int64:dst_end = dst + n;", "any->:dst_end = @cast_unchecked<any->>(@cast_unchecked<int64>(dst) + n);"),

    # memcpy calls
    ("drop(mem_memcpy(r, src, alloc_size));", "Result<any->>:_r_mc = mem_memcpy(@cast_unchecked<any->>(r), src, alloc_size);\n    any->:r_ptr = @cast_unchecked<any->>(r);"),
    ("drop(mem_memcpy(r, src, actual_len));", "Result<any->>:_r_mc = mem_memcpy(@cast_unchecked<any->>(r), src, actual_len);\n    any->:r_ptr = @cast_unchecked<any->>(r);"),
    ("pass r;", "pass @cast_unchecked<any->>(r);"),

    ("int64:n = raw str_strlen(src);", "int64:n = raw str_strlen(src);"),
    ("int64:actual_len = raw str_strnlen(src, n);", "int64:actual_len = raw str_strnlen(src, n);"),
    ("(@cast_unchecked<uint8->>(r))[actual_len] = 0u8;", "(@cast_unchecked<uint8->>(r))[actual_len] = 0u8;")
]

for old, new in replacements:
    text = text.replace(old, new)

with open('src/str/strcpy.npk', 'w') as f:
    f.write(text)

