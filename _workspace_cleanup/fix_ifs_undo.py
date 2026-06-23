import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig_code = code

    # Fix: else if ((cond) { -> else if (cond) {
    code = re.sub(r'else\s+if\s+\(\(([^)]+)\)', r'else if (\1)', code)

    # Fix: if ((cond) { -> if (cond) {
    code = re.sub(r'\bif\s+\(\(([^)]+)\)', r'if (\1)', code)

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed double parens in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
