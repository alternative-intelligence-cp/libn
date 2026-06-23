import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Change `uint8[]:var = "string"` to `string:var = "string"`
    code = re.sub(r'uint8\[\]:([a-zA-Z0-9_]+)\s*=\s*("[^"]+");', r'string:\1 = \2;', code)

    # Change `@cast_unchecked<int64>(@pfx[0])` to `@cast_unchecked<int64>(pfx)` if pfx is now a string
    # Just globally replace `@cast_unchecked<int64>\(@([a-zA-Z0-9_]+)\[0\]\)` with `@cast_unchecked<int64>(\1)`
    # BUT wait, this will break arrays like `tmpl`!
    # Because `tmpl` is an array! `uint8[32]:tmpl`
    # So we should only replace for specific strings: `pfx` and `TMP_DIR` and `TMP_PREFIX`
    code = code.replace('@cast_unchecked<int64>(@pfx[0])', '@cast_unchecked<int64>(pfx)')
    code = code.replace('@cast_unchecked<int64>(@TMP_DIR[0])', '@cast_unchecked<int64>(TMP_DIR)')
    code = code.replace('@cast_unchecked<int64>(@TMP_PREFIX[0])', '@cast_unchecked<int64>(TMP_PREFIX)')
    code = code.replace('@cast_unchecked<int64>(@hex[0])', '@cast_unchecked<int64>(hex)')
    code = code.replace('@cast_unchecked<int64>(@prefix[0])', '@cast_unchecked<int64>(prefix)')

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
