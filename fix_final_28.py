import os, glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # 1. Replace pass with return or exit where appropriate
    if 'main' in file or 'test_all' in file:
        text = text.replace('pass 0i32;', 'exit 0i64;')
        text = text.replace('pass 0i64;', 'exit 0i64;')
    
    # 2. Add missing semicolons after function blocks
    text = re.sub(r'\}\s*\n\s*pub func', r'};\n\npub func', text)
    text = re.sub(r'\}\s*\n\s*func', r'};\n\nfunc', text)
    # specific fix for strfmt.npk ending functions without ;
    text = text.replace('5i64));\n}\n', '5i64));\n};\n')
    text = text.replace('7i64));\n}\n', '7i64));\n};\n')
    text = text.replace('a7);\n}', 'a7);\n};')

    # 3. Replace => casts with @cast_unchecked
    def replace_cast(m):
        val = m.group(1).strip()
        typ = m.group(2).strip()
        # Ensure we add space to avoid ->>
        if typ.endswith('->'):
            return f'@cast_unchecked<{typ} >({val})'
        return f'@cast_unchecked<{typ}>({val})'
    
    text = re.sub(r'(\([^\)]+\)|@?"?[a-zA-Z0-9_/\.\-]+"?\[[0-9]+\]|@?[a-zA-Z0-9_/\.\-]+)\s*=>\s*([a-zA-Z0-9_\->]+)', replace_cast, text)
    
    # 4. Fix any ->> that were already there
    text = text.replace('->>', '-> >')

    # 5. Restore memcpy.npk line 60 comment that might have been hit
    text = text.replace('@cast_unchecked<int64-> >(aligned', 'aligned')
    
    # 6. Restore exec.npk
    text = text.replace('@cast_unchecked<int64>(permitted', 'permitted')
    text = text.replace('@cast_unchecked<int64>(director', 'director')
    text = text.replace('@cast_unchecked<int64>(process', 'process')
    text = text.replace('@cast_unchecked<int64>(call', 'call')
    text = text.replace('@cast_unchecked<int64>(error', 'error')
    text = text.replace('@cast_unchecked<int64>(addres', 'addres')
    
    # 7. str_snprintf calls in printf.npk and strbuf.npk
    text = text.replace('int64:msg = _!err_str@cast_unchecked<int64>((e));', 'int64:msg = _!err_str(e);')

    with open(file, 'w') as f:
        f.write(text)

with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('pass 0i32;', 'exit 0i64;')
text = text.replace('pass 0i64;', 'exit 0i64;')
text = text.replace('pass;', 'exit 0i64;')
with open('test_all.npk', 'w') as f:
    f.write(text)

