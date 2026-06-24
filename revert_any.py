import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Replace @cast_unchecked<any->>(expr) with expr
    # We must match matching parentheses if possible, but regex can't easily.
    # However, in Nitpick, these casts are usually simple: @cast_unchecked<any->>(foo)
    # Let's write a small parser for the parentheses.
    
    def remove_cast(text):
        res = ""
        i = 0
        while i < len(text):
            target = "@cast_unchecked<any->>("
            if text.startswith(target, i):
                i += len(target)
                # Find matching parenthesis
                depth = 1
                start = i
                while i < len(text) and depth > 0:
                    if text[i] == '(': depth += 1
                    elif text[i] == ')': depth -= 1
                    i += 1
                # i is now right after the matching ')'
                inner = text[start:i-1]
                res += inner
            else:
                res += text[i]
                i += 1
        return res

    content = remove_cast(content)

    # 2. Replace any-> with int64 everywhere
    content = content.replace("any->", "int64")

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Reverted in {filepath}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
