import os
import re

def fix_pick(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_pick = False
    pick_var = ""
    first_case = True

    for line in lines:
        if not in_pick:
            m = re.match(r'^(\s*)pick\s+([a-zA-Z0-9_]+)\s*\{', line)
            if m:
                in_pick = True
                pick_var = m.group(2)
                first_case = True
                out.append(m.group(1) + "// Replaced pick\n")
            else:
                out.append(line)
        else:
            m = re.match(r'^(\s*)([^=\s]+)\s*=>\s*(.+)', line)
            if m:
                indent = m.group(1)
                val = m.group(2)
                expr = m.group(3)
                
                if val == '_':
                    out.append(f"{indent}else {{ {expr} }}\n")
                else:
                    kw = "if" if first_case else "else if"
                    first_case = False
                    out.append(f"{indent}{kw} ({pick_var} == {val}) {{ {expr} }}\n")
            elif re.match(r'^\s*\}\s*;?\s*$', line):
                in_pick = False
                # out.append(line)  # We replaced pick with if blocks, no closing brace needed for the switch itself
            else:
                out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_pick(os.path.join(root, f))
