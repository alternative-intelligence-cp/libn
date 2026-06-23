import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # 1. Fix if/while parens
    # Match 'if ' or 'while ', followed by anything up to '{', not containing '{'
    # We must be careful about nested braces, but conditions don't have braces in Nitpick.
    # We also must ensure we don't double-wrap.
    def wrap_cond(match):
        keyword = match.group(1)
        cond = match.group(2).strip()
        if cond.startswith('(') and cond.endswith(')'):
            return f"{keyword} {cond} {{"
        return f"{keyword} ({cond}) {{"
    
    content = re.sub(r'\b(if|while)\s+([^{]+?)\s*\{', wrap_cond, content)

    # 2. Fix closing semicolons for functions.
    # In Nitpick, `pub func` or `func` ends with `}`. We want `};`
    # We can just blindly replace `\n}\n` at the end of functions.
    # Actually, simpler: replace `\n}\n` with `\n};\n` globally? NO, that breaks if/while loops.
    # Let's run compiler and fix `Expected ';' after function declaration` lines automatically.
    
    # 3. Fix pointers
    content = content.replace('*byte', 'uint8->')
    content = content.replace('*int64', 'int64->')
    content = content.replace('*uint64', 'uint64->')
    content = content.replace('*int32', 'int32->')
    content = content.replace('*uint32', 'uint32->')
    content = content.replace('*uint8', 'uint8->')
    content = content.replace('*int8', 'int8->')

    # 4. Fix `as` casts
    # Match: `X as Y` -> `@cast_unchecked<Y>(X)`
    # This is tricky with regex. Let's find simple ones like `x as y;`
    content = re.sub(r'([A-Za-z0-9_\[\]\+\-\*&]+(?:\s*[-+*&]\s*[A-Za-z0-9_\[\]]+)?(?:\([^\)]*\))?)\s+as\s+([a-zA-Z0-9_\-]+(?:->)?)', r'@cast_unchecked<\2>(\1)', content)
    
    with open(path, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

