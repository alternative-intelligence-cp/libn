import os

with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()

target = """        f.buf_len = r.value;
        if (r.value == 0i64) {
            f.flags = f.flags | FILE_FLAG_EOF;
        }
        pass r.value; }
    pass 0i64; } pass 0i64;
    }"""

replacement = """        int64:v = 0i64;
        if (!r.is_error) { v = r.value; }
        f.buf_len = v;
        if (v == 0i64) {
            f.flags = f.flags | FILE_FLAG_EOF;
        }
        pass v;
    }"""

if target in code:
    code = code.replace(target, replacement)
else:
    print("WARNING: target not found!")
    
with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer11.py")
