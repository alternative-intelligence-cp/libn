import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig_code = code

    # Fix: else if cond { -> else if (cond) {
    # Match 'else if ' followed by anything not starting with ( and ending with {
    def fix_else_if(m):
        cond = m.group(1).strip()
        return f"else if ({cond}) {{"
    
    code = re.sub(r'else\s+if\s+([^{]+?)\s*\{', fix_else_if, code)

    # Fix: if cond { -> if (cond) {
    # Match 'if ' followed by anything not starting with ( and ending with {
    def fix_if(m):
        cond = m.group(1).strip()
        # if cond is already in parens, don't wrap again
        if cond.startswith('(') and cond.endswith(')'):
            return f"if {cond} {{"
        return f"if ({cond}) {{"
    
    code = re.sub(r'\bif\s+([^{]+?)\s*\{', fix_if, code)

    # Note: re.sub above might match 'if (cond) {' and wrap it to 'if ((cond)) {'.
    # The fix_if function checks for starts/ends with parens.

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed ifs in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
