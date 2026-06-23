import re
with open("src/mem/slab.npk", "r") as f:
    content = f.read()

# Fix if i == 0i64 { -> if (i == 0i64) {
content = re.sub(r'if i == ([0-9]+i64) \{', r'if (i == \1) {', content)

# Fix Result pass
content = re.sub(r'Result<int64>:r = mem_free\(ptr\);\n\s*pass r;', r'Result<int64>:r = mem_free(ptr);\n        if (r.is_error) { fail r.error; }\n        pass r.value;', content)

# Fix pointers
content = content.replace('*int64:next_ptr = ptr as *int64;', 'int64->:next_ptr = @cast_unchecked<int64->>(ptr);')
content = content.replace('*byte:p    = ptr as *byte;', 'byte->:p = @cast_unchecked<byte->>(ptr);')

# Fix while zi < sz
content = content.replace('while zi < sz {', 'while (zi < sz) {')

with open("src/mem/slab.npk", "w") as f:
    f.write(content)
