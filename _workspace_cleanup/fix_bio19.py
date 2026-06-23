import os
import re

def fix():
    # 1. strcpy.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strcpy.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace(
        "Result<int64>:r = slab_alloc(alloc_size);\n    if (r.is_error) {\n        fail r.error;\n    }\n\n    // Copy including NUL terminator\n    drop mem_memcpy(r.value, src, alloc_size);\n\n    pass r.value;",
        "int64:r = slab_alloc(alloc_size);\n    if (r == 0i64) { pass 0i64; }\n    drop mem_memcpy(r, src, alloc_size);\n    pass r;"
    )
    content = content.replace(
        "Result<int64>:r = slab_alloc(alloc_size);\n    if (r.is_error) {\n        fail r.error;\n    }\n\n    drop mem_memcpy(r.value, src, actual_len);\n    (@cast_unchecked<uint8->>(r.value))[actual_len] = 0u8;\n\n    pass r.value;",
        "int64:r = slab_alloc(alloc_size);\n    if (r == 0i64) { pass 0i64; }\n    drop mem_memcpy(r, src, actual_len);\n    (@cast_unchecked<uint8->>(r))[actual_len] = 0u8;\n    pass r;"
    )
    with open(path, "w") as f: f.write(content)

    # 2. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace('use "src/str/strfmt.npk".*;', 'use "src/str/strfmt.npk".*;\nuse "src/syscall/errno.npk".*;')
    content = content.replace("endptr != 0i64", "@cast_unchecked<int64>(endptr) != 0i64")
    content = content.replace("while (is_whitespace(p[i]))", "while (raw is_whitespace(p[i]))")
    content = content.replace("int64:dv = digit_val(p[i], base);", "int64:dv = raw digit_val(p[i], base);")
    content = content.replace("ERR_RANGE", "ERANGE")
    content = content.replace("@cast_unchecked<int64->>(ep)", "@cast_unchecked<int64->>(@ep[0])")
    content = content.replace("Result<int64>:r = math_sat_add_u64", "int64:r = math_sat_add_u64")
    content = content.replace("Result<int64>:r = math_sat_sub_u64", "int64:r = math_sat_sub_u64")
    content = content.replace("if (r.value ==", "if (r ==")
    content = content.replace("result = r.value;", "result = r;")
    with open(path, "w") as f: f.write(content)

fix()
