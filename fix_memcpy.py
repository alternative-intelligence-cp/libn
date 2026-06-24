import re

with open('src/mem/memcpy.npk', 'r') as f:
    content = f.read()

content = content.replace("pub func:__intrinsic_memcpy = int64(", "pub func:__intrinsic_memcpy = bool(")
content = content.replace("    pass 0i64;\n};", "    pass false;\n};")

content = content.replace("""    if (num_bytes >= 16i64) {
        drop(__intrinsic_memcpy(dst, src, num_bytes));
        pass dst;
    }""", """    if (num_bytes >= 16i64) {
        if (__intrinsic_memcpy(dst, src, num_bytes)) {
            pass dst;
        }
    }""")

with open('src/mem/memcpy.npk', 'w') as f:
    f.write(content)
