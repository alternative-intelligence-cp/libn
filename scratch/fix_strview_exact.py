import re

# Read lines
with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()

with open('scratch/strview_errors.txt', 'r') as f:
    errors = f.read()

updates = {}

# Regex to find: Line (\d+), Column (\d+)
for match in re.finditer(r'Line (\d+), Column (\d+)', errors):
    line_idx = int(match.group(1)) - 1
    col_idx = int(match.group(2)) - 1
    
    if line_idx not in updates:
        updates[line_idx] = []
    updates[line_idx].append(col_idx)

for line_idx in sorted(updates.keys()):
    line = lines[line_idx]
    # Sort columns descending to avoid shifting issues when inserting
    for col_idx in sorted(updates[line_idx], reverse=True):
        # find the argument: alphanumeric + '_' + '->' + '.' + '[' + ']' (simple)
        # We can just match a simple expression
        m = re.match(r'([a-zA-Z0-9_>.-]+)', line[col_idx:])
        if m:
            arg = m.group(1)
            # wait, if arg is something like `s->ptr`, it captures it perfectly.
            # but if there are spaces or it's `@cast...`, well, the compiler wouldn't complain if it was already `any->`
            line = line[:col_idx] + f'@cast_unchecked<any->>({arg})' + line[col_idx + len(arg):]
    lines[line_idx] = line

with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)

