import os
import re

for root, _, files in os.walk('src'):
    for f in files:
        if not f.endswith('.npk'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r') as fp:
            content = fp.read()
            
        # Replace `func:name = Result<TYPE>(` with `func:name = TYPE(`
        # We might have `pub func:` or just `func:`.
        # Also need to match generic functions like `func<T>:...`
        new_content = re.sub(r'(= \s*)Result<([a-zA-Z0-9_\*\[\]\->]+)>\s*\(', r'\1\2(', content)
        
        if new_content != content:
            with open(path, 'w') as fp:
                fp.write(new_content)
                print(f"Fixed {path}")

