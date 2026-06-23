import os
import re

def fix_address_of(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Replace &identifier or &identifier[index] with @identifier
    # We must be careful not to match spaces (which would be bitwise AND)
    # Also handle &@cast... if that exists
    
    # Matches `&name` -> `@name`
    code = re.sub(r'&([a-zA-Z_][a-zA-Z0-9_]*(\[[^\]]+\])?)', r'@\1', code)
    
    # Matches `&@cast` -> `@@cast`. Uses non-greedy `.+?` to handle types like `FILE->`
    code = re.sub(r'&(@cast_unchecked<.+?>\([^)]+\))', r'@\1', code)

    # Matches `&"string"` -> `@"string"`
    code = re.sub(r'&("[^"]*"(\[[^\]]+\])?)', r'@\1', code)
    
    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed address-of in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_address_of(os.path.join(root, f))
