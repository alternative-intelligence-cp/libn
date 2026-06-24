import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Replace any-> with int64 in function signatures and variable declarations
    content = content.replace("any->", "int64")
    
    # Now we have @cast_unchecked<int64>(0i64) from the above replacement
    # We want to change @cast_unchecked<int64>(0i64) to 0i64
    content = content.replace("@cast_unchecked<int64>(0i64)", "0i64")

    # The user also wants to remove @cast_unchecked<int64>(ptr) where ptr is already int64?
    # It's safer to just leave the redundant casts unless the compiler complains.
    # The auditor explicitly called out `@cast_unchecked<any->>(0i64)`.

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Reverted in {filepath}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
