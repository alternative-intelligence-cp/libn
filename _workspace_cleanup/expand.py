import re

def resolve_use(filepath, visited=None):
    if visited is None: visited = set()
    if filepath in visited: return ""
    visited.add(filepath)
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        return f"// ERROR reading {filepath}: {e}\n"
    out = []
    for line in lines:
        m = re.match(r'^\s*use\s+"([^"]+)"\.\*;\s*', line)
        if m:
            out.append(f"// --- BEGIN {m.group(1)} ---\n")
            out.append(resolve_use(m.group(1), visited))
            out.append(f"// --- END {m.group(1)} ---\n")
        else:
            out.append(line)
    return "".join(out)

with open("expanded.npk", "w") as f:
    f.write(resolve_use("test_root.npk"))
