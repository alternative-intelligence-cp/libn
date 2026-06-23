import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Address of variable: Replace &var with @var
    # We should be careful to only replace & that acts as address-of.
    # In Nitpick, bitwise AND is `a & b`. So if `&` is preceded by an operator, `(`, `,`, `[`, `=`, or start of line/space.
    # Actually, we can just replace `&[a-zA-Z_]` with `@[a-zA-Z_]`? No, we might have `&candidate`.
    
    # Let's fix the @cast_unchecked<int64>(&argv[0]) to @cast_unchecked<int64>(@argv[0])
    content = content.replace('&@cast_unchecked', '@cast_unchecked')
    # Wait, earlier I replaced &@cast_unchecked<int64>(...) with @cast_unchecked<int64>(&...)
    # Now I should just replace `&` inside those casts with `@`.
    content = re.sub(r'@cast_unchecked<([^>]+)>\(&([^)]+)\)', r'@cast_unchecked<\1>(@\2)', content)
    
    # Also fix other remaining `&var` in the file.
    # This regex matches `&` followed by an identifier.
    content = re.sub(r'(?<![a-zA-Z0-9_])&([a-zA-Z_])', r'@\1', content)
    
    with open(path, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

