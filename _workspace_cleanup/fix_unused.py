import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Prefix drop to lines that are just function calls
    # Match: start of line, whitespace, an identifier, open parenthesis
    # Exclude: drop, pass, fail, return, continue, break, if, while, for, switch, func, pub
    # Exclude definitions like `pub func:foo = ...`
    code = re.sub(
        r'^(\s*)(?!drop\b|pass\b|fail\b|return\b|continue\b|break\b|if\b|while\b|for\b|switch\b|func\b|pub\b)([a-zA-Z0-9_]+)\(',
        r'\1drop \2(',
        code,
        flags=re.MULTILINE
    )

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
