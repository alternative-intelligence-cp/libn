import os, glob, re

def replace_cast(m):
    val = m.group(1).strip()
    typ = m.group(2).strip()
    return f'@cast_unchecked<{typ}>({val})'

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    # Matches: (s + i) => int64->
    # Matches: @argv[0] => int64
    # Matches: @"/bin/sh"[0] => int64
    # Matches: f[fi] => int64
    text = re.sub(r'(\([^\)]+\)|@?"?[a-zA-Z0-9_/\.\-]+"?\[[0-9]+\]|@?[a-zA-Z0-9_/\.\-]+)\s*=>\s*([a-zA-Z0-9_\->]+)', replace_cast, text)

    with open(file, 'w') as f:
        f.write(text)

