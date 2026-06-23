import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Fix `if condition {` -> `if (condition) {`
    # Also `else if condition {` -> `else if (condition) {`
    # Ensure it only matches if there are no parens already (by excluding '(' and ')')
    
    content = re.sub(r'(?<!else )if\s+([^{()]+)\s+\{', r'if (\1) {', content)
    content = re.sub(r'else if\s+([^{()]+)\s+\{', r'else if (\1) {', content)
    content = re.sub(r'while\s+([^{()]+)\s+\{', r'while (\1) {', content)

    with open(filepath, "w") as f:
        f.write(content)

fix_file("src/mem/slab.npk")
fix_file("src/syscall/syscall.npk")
