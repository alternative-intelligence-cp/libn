import re

with open('/home/randy/Workspace/REPOS/libn/src/math/math.npk', 'r') as f:
    content = f.read()

# We need to replace math_abs_i64(a) with raw math_abs_i64(a)
# But only if not already preceded by raw

def add_raw(match):
    prefix = match.group(1)
    func = match.group(2)
    args = match.group(3)
    if 'raw' in prefix[-4:]:
        return match.group(0)
    return f"{prefix}raw {func}{args}"

# Matches math_*(...)
content = re.sub(r'([^a-zA-Z0-9_])(math_[a-zA-Z0-9_]+)(\([^)]*\))', add_raw, content)

with open('/home/randy/Workspace/REPOS/libn/src/math/math.npk', 'w') as f:
    f.write(content)

