import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig_code = code

    # 1. Rename 'limit' variable to 'limit_val'
    code = re.sub(r'\blimit\b', 'limit_val', code)

    # 2. Fix double closing parenthesis in function declarations:
    # e.g., pub func:mem_is_zero = bool(int64:ptr, int64:n)) {
    code = re.sub(r'\)\)\s*\{', r') {', code)

    # 3. Fix memutil.npk:227 "Expected ';' after function declaration. Found: identifier 'i'"
    # It might be `for int64:i = 0`? Wait, let's fix missing semicolons.
    # We can just see if it compiles first.

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed remaining syntax in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
