import re
import json

with open('src/math/math.npk', 'r') as f:
    lines = f.readlines()

chunks = []
for i, line in enumerate(lines):
    if re.search(r'\bpass\b', line):
        if 'pass(' in line:
            continue
        # match `pass expr;`
        m = re.search(r'pass\s+(.+?);', line)
        if m:
            expr = m.group(1)
            orig = f"pass {expr};"
            new = f"pass({expr});"
            chunks.append({
                "StartLine": i + 1,
                "EndLine": i + 1,
                "TargetContent": orig,
                "ReplacementContent": new,
                "AllowMultiple": True
            })

print(json.dumps(chunks))
