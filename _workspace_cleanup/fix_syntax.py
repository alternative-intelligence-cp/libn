import os, re

def check_balanced(s):
    depth = 0
    for char in s:
        if char == '(': depth += 1
        elif char == ')': depth -= 1
        if depth < 0: return False
    return depth == 0

def fully_wrapped(cond):
    cond = cond.strip()
    if not (cond.startswith('(') and cond.endswith(')')):
        return False
    inner = cond[1:-1]
    return check_balanced(inner)

def process(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    def repl_elif(m):
        prefix = m.group(1)
        cond = m.group(2).strip()
        if not fully_wrapped(cond):
            return f"{prefix}else if ({cond}) {{"
        return m.group(0)

    content = re.sub(r'(\b)else if\s+([^{]+?)\s*\{', repl_elif, content)

    def repl_if(m):
        prefix = m.group(1)
        cond = m.group(2).strip()
        if not fully_wrapped(cond):
            return f"{prefix}if ({cond}) {{"
        return m.group(0)

    content = re.sub(r'(\b)if\s+([^{]+?)\s*\{', repl_if, content)

    def repl_while(m):
        prefix = m.group(1)
        cond = m.group(2).strip()
        if not fully_wrapped(cond):
            return f"{prefix}while ({cond}) {{"
        return m.group(0)

    content = re.sub(r'(\b)while\s+([^{]+?)\s*\{', repl_while, content)

    with open(filepath, "w") as f:
        f.write(content)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process(os.path.join(root, file))
