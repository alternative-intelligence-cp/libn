import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace `as *uint8` with `@cast_unchecked<uint8->>`
    # e.g., `value as *uint8` -> `@cast_unchecked<uint8->>(value)`
    # This is tricky with regex. Let's do a simple replace for `*uint8:` to `uint8->:`
    new_content = re.sub(r'\*uint8:', 'uint8->:', content)
    
    # Replace `as *uint8`
    # Let's find patterns like `(\w+) as \*uint8` and replace with `@cast_unchecked<uint8->>(\1)`
    # Or `\(([^)]+)\) as \*uint8` -> `@cast_unchecked<uint8->>(\1)`
    # Let's write a targeted function
    
    def replace_as_ptr(match):
        expr = match.group(1)
        return f'@cast_unchecked<uint8->>({expr})'

    new_content = re.sub(r'\b([a-zA-Z0-9_]+)\s+as\s+\*uint8\b', replace_as_ptr, new_content)
    # Handle parens: `(expr) as *uint8`
    new_content = re.sub(r'\(([^)]+)\)\s+as\s+\*uint8\b', replace_as_ptr, new_content)

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
