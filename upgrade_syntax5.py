import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    def repl_cond(m):
        kw = m.group(1)
        cond = m.group(2).strip()
        # Avoid double parens if it already has them
        if cond.startswith('(') and cond.endswith(')'):
            # But wait, what if `(a == 1) || (b == 2)`?
            # If it starts with '(' and ends with ')', we still need to make sure the WHOLE thing is wrapped.
            # We can just check if it's already wrapped, but wait! The previous scripts might have wrapped it partially.
            # It's safer to just wrap it in `(` `)` if it's not EXACTLY what was there.
            # Actually, `cond` might be `(a == 1) || (b == 2)`. It starts and ends with parens, but they don't match each other!
            # Let's count parens.
            depth = 0
            is_wrapped = True
            for i, c in enumerate(cond):
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                if depth == 0 and i < len(cond) - 1:
                    is_wrapped = False
                    break
            if is_wrapped and cond.startswith('('):
                return f"{kw} {cond} {{"
        return f"{kw} ({cond}) {{"

    content = re.sub(r'\b(if|while)\s+([^\{]+?)\s*\{', repl_cond, content)
    
    with open(path, 'w') as f:
        f.write(content)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

