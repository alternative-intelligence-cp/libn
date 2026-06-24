import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Replace "pass some_func(...);" with "return some_func(...);"
    # specifically targeting common prefixes: libn_, io_, mem_, str_, strbuf_, strview_, math_
    # or just any word ending in (
    # We must be careful not to match `pass (foo);`
    
    # We want to match: `pass name(` where name is a valid identifier
    # excluding keywords like `@cast_unchecked`
    
    content = re.sub(r'pass\s+([a-zA-Z_][a-zA-Z0-9_]*)\(', r'return \1(', content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
