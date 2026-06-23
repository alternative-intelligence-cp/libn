import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Fix corrupted comments that were incorrectly captured as C-style casts
    # E.g., `@cast_unchecked<or we exhaust n>(while)` -> `(or we exhaust n)\n    while`
    # We will use a regex that looks for @cast_unchecked<text with spaces>(keyword)
    
    def fix_cast_corruption(m):
        inner = m.group(1)
        next_word = m.group(2)
        if ' ' in inner or inner in ['blocking', 'background', 'input']:
            # It's a comment
            return f"({inner})\n    {next_word}"
        return m.group(0)

    code = re.sub(r'@cast_unchecked<([^>]+)>\(([a-zA-Z0-9_]+)\)', fix_cast_corruption, code)

    # Some cases might be `@cast_unchecked<blocking>(or)`
    code = code.replace('@cast_unchecked<blocking>(or)', '(blocking) or')
    code = code.replace('@cast_unchecked<input>(and)', '(input) and')
    code = code.replace('@cast_unchecked<a>(not)', '(a) not')
    code = code.replace('@cast_unchecked<an>(but)', '(an) but')
    code = code.replace('@cast_unchecked<not omitted>(to)', '(not omitted) to')

    # Re-apply function closing brace semicolons if they got messed up
    # (they shouldn't have been)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed corruption in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
