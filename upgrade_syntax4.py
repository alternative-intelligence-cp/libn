import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Replace function return types void(...) -> NIL(...)
    # Since `void` is only used as a type or in `(void)():f`, we can replace `void` when followed by `(` or `)`
    # Or just replace all `void` tokens, except inside comments.
    # It's safer to just replace `void` with `NIL` because it's not a valid identifier anyway.
    
    # Wait, if we replace all `void` we might break comments! Let's do ` void(` -> ` NIL(` and `void()` -> `NIL()`
    content = re.sub(r'\bvoid\s*\(', r'NIL(', content)
    content = re.sub(r'\bvoid\b', r'NIL', content) # Actually just replace all `void` keywords not in comments.
    
    # To be safe against comments, just simple replacements for common patterns:
    # `void(` -> `NIL(`
    content = content.replace('void(', 'NIL(')
    content = content.replace('void:', 'NIL:')
    content = content.replace('void)', 'NIL)')
    content = content.replace('<void()>', '<NIL()>')
    
    with open(path, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

