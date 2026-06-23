import os, glob, re

for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()
        
    # Fix `if condition {` -> `if (condition) {`
    s = re.sub(r'if\s+([^{]*?)\s*\{', r'if (\1) {', s)
    # Fix `while condition {` -> `while (condition) {`
    s = re.sub(r'while\s+([^{]*?)\s*\{', r'while (\1) {', s)

    # Undo double parens
    s = re.sub(r'if\s+\(\((.*?)\)\)\s*\{', r'if (\1) {', s)
    s = re.sub(r'while\s+\(\((.*?)\)\)\s*\{', r'while (\1) {', s)
    s = re.sub(r'if\s+\(\(\((.*?)\)\)\)\s*\{', r'if (\1) {', s)
    s = re.sub(r'while\s+\(\(\((.*?)\)\)\)\s*\{', r'while (\1) {', s)

    with open(filepath, 'w') as f:
        f.write(s)
