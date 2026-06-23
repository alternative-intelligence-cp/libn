import re

with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

def fix_if_while(t):
    lines = t.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        m = re.match(r'^(\s*(?:if|while|else if)\s*)([^{]+)(\s*\{\s*)$', line)
        if m:
            cond = m.group(2).strip()
            if not (cond.startswith('(') and cond.endswith(')')):
                lines[i] = f"{m.group(1)}({cond}){m.group(3)}"
    return '\n'.join(lines)

text = fix_if_while(text)

# Also fix `else if` on same line as `}`
def fix_else_if(t):
    lines = t.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        m = re.match(r'^(\s*\}\s*else if\s*)([^{]+)(\s*\{\s*)$', line)
        if m:
            cond = m.group(2).strip()
            if not (cond.startswith('(') and cond.endswith(')')):
                lines[i] = f"{m.group(1)}({cond}){m.group(3)}"
    return '\n'.join(lines)

text = fix_else_if(text)

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)
