import os
import re

def rewrite_file(path):
    with open(path, 'r') as f:
        code = f.read()
    
    orig_code = code

    # Fix: struct Name { -> struct:Name = {
    # e.g., pub struct FILE {
    code = re.sub(r'\bstruct\s+([A-Za-z0-9_]+)\s*\{', r'struct:\1 = {', code)

    # Some might not have pub, regex handles that since \bstruct\s+ matches struct alone
    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed structs in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                rewrite_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
