import re

def resolve_use(filepath, visited=None):
    if visited is None: visited = set()
    if filepath in visited: return ""
    visited.add(filepath)
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        return ""
    out = []
    for line in lines:
        m = re.match(r'^\s*use\s+"([^"]+)"\.\*;\s*', line)
        if m:
            out.append(resolve_use(m.group(1), visited))
        else:
            out.append(line)
    return "".join(out)

with open("expanded_exact.npk", "w") as f:
    f.write(resolve_use("test_root.npk"))
