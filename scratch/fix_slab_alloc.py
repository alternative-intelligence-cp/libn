import re

with open('src/mem/slab.npk', 'r') as f:
    text = f.read()

replacement = """        Result<int64>:r = mem_malloc(n);
        if (r.is_error) { pass 0i64; }
        pass r.value;"""

text = re.sub(r'Result<int64>:r = mem_malloc\(n\);\n\s*return r;', replacement, text, flags=re.DOTALL)

with open('src/mem/slab.npk', 'w') as f:
    f.write(text)

