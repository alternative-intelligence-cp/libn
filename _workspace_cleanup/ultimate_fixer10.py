import re

with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()

# Fix the mess with r.value accesses
# First, revert the messy if blocks back to simple pass r.value
code = re.sub(r'if \(!r.is_error\) \{ if \(!r.is_error\).*?pass 0i64;', 'pass r.value;', code, flags=re.DOTALL)
code = code.replace('pass r.value;\n    }', 'pass r.value;\n    }')
# No wait, regex with DOTALL might eat too much of the file! Let's be exact.

code = code.replace(
'''        f.buf_len = r.value;
        if (r.value == 0i64) {
            f.flags = f.flags | FILE_FLAG_EOF;
        }
        if (!r.is_error) { if (!r.is_error) { pass r.value; }
    pass 0i64; }
    pass 0i64; } pass 0i64;
    }''',
'''        int64:v = 0i64;
        if (!r.is_error) { v = r.value; }
        f.buf_len = v;
        if (v == 0i64) {
            f.flags = f.flags | FILE_FLAG_EOF;
        }
        pass v;
    }'''
)

# And if there's any other "if (!r.is_error) { if (!r.is_error)"
code = re.sub(r'if \(!r\.is_error\) \{\s*if \(!r\.is_error\) \{\s*pass r\.value;\s*\}\s*pass 0i64;\s*\}', r'if (!r.is_error) { pass r.value; } pass 0i64;', code)

with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer10.py")
