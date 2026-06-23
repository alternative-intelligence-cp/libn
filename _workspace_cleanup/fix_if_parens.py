import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig = code

    # Catch any generic if (expr) OP expr {
    code = re.sub(r'if\s*\(([^)]+)\)\s*(!=|==|>|<|>=|<=)\s*([a-zA-Z0-9_]+)\s*\{', r'if ((\1) \2 \3) {', code)
    code = re.sub(r'while\s*\(([^)]+)\)\s*(!=|==|>|<|>=|<=)\s*([a-zA-Z0-9_]+)\s*\{', r'while ((\1) \2 \3) {', code)

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)
        print("Fixed if parens in", path)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
