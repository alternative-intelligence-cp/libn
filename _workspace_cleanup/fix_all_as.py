import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Match `(expr as type)` where expr can contain spaces but no parens or commas
    code = re.sub(r'\(([^(),]+)\s+as\s+([a-zA-Z0-9_*]+)\)', r'(@cast_unchecked<\2>(\1))', code)

    # Match string literal casts: `@"string"[0] as type` or `"string" as type`
    code = re.sub(r'(@?"[^"]*"(?:\[\d+\])?)\s+as\s+([a-zA-Z0-9_*]+)', r'@cast_unchecked<\2>(\1)', code)

    # Match `expr as type` without parens, assuming simple identifiers or arr[index]
    code = re.sub(r'(?<![A-Za-z0-9_\]])([@]?[a-zA-Z0-9_]+(?:\[[^\]]*\])?)\s+as\s+([a-zA-Z0-9_*]+)', r'@cast_unchecked<\2>(\1)', code)

    # Match `(expr) as type`: e.g. `(a + i) as *int64`
    code = re.sub(r'\(([^)]+)\)\s+as\s+([a-zA-Z0-9_*]+)', r'@cast_unchecked<\2>(\1)', code)

    # Clean up `*type` -> `type->` inside casts
    code = re.sub(r'@cast_unchecked<\*([a-zA-Z0-9_]+)>', r'@cast_unchecked<\1->>', code)

    # Wait, there's also `byte` to `uint8` inside casts
    code = re.sub(r'@cast_unchecked<byte->>', r'@cast_unchecked<uint8->>', code)
    code = re.sub(r'@cast_unchecked<byte>', r'@cast_unchecked<uint8>', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed casts in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
