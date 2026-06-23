import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Ternary operators (buf_space < remaining ? buf_space : remaining)
    if 'int64:to_copy = buf_space < remaining ? buf_space : remaining;' in content:
        ternary = """int64:to_copy = 0i64;
        if (buf_space < remaining) { to_copy = buf_space; } else { to_copy = remaining; }"""
        content = content.replace('int64:to_copy = buf_space < remaining ? buf_space : remaining;', ternary)

    # 2. Pointers and casts: (dst as *byte)[...] -> @cast_unchecked<uint8->>(dst)[...]
    content = re.sub(r'\(([a-zA-Z0-9_]+)\s+as\s+\*byte\)\[', r'@cast_unchecked<uint8->>(\1)[', content)
    # also `f.unget as byte` -> `@cast_unchecked<uint8>(f.unget)`
    content = content.replace('f.unget as byte', '@cast_unchecked<uint8>(f.unget)')
    
    # 3. int64:e = wr.err as int64;
    content = re.sub(r'int64:([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)\.err as int64;', r'int64:\1 = @cast_unchecked<int64>(\2.error);', content)

    # 4. Missing parentheses on `if e == EINTR`
    content = re.sub(r'if\s+([a-zA-Z0-9_]+\s*==\s*[a-zA-Z0-9_]+)\s+\{', r'if (\1) {', content)
    
    # Also `if (f.flags & FILE_FLAG_READ_MODE) == 0i64 {`
    # Our previous regex for `if` might have failed because we used ^(\s*)if. In fio.npk, some ifs are indented differently or have leading stuff?
    # Let's just do a blanket replace for known bad ones:
    content = content.replace('if f.buf_pos > 0i64 {', 'if (f.buf_pos > 0i64) {')
    content = content.replace('if e == EINTR {', 'if (e == EINTR) {')

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src/io/bio'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
