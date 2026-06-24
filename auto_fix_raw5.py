import os
import re

with open('/home/randy/.gemini/antigravity/brain/8b6833ba-693e-4e81-9a6d-fea45d4d0319/.system_generated/tasks/task-9496.log', 'r') as f:
    err_text = f.read()

# Load all files
files_cache = {}
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                files_cache[path] = f.read().splitlines()

errors = re.findall(r"Cannot silently unwrap Result<int64> into '([^']+)'", err_text)
# We can't rely on Line numbers because they are relative to all.npk which is just `use` statements!
# Wait, no. The line numbers in `task-9496.log` for these specific errors are line numbers in `all.npk`, which is completely useless.
# But we can just search for the variable name assignments!
var_names = set(errors)

for var_name in var_names:
    for path, lines in files_cache.items():
        for i, line in enumerate(lines):
            # Look for `int64:{var_name} = ` or similar
            if re.search(r'\b' + var_name + r'\s*=', line) and not 'raw ' in line and not '==' in line and not '!=' in line and not '<=' in line and not '>=' in line and not '+=' in line:
                idx_eq = line.find('=')
                if idx_eq != -1:
                    # skip if it's a simple literal or math
                    if '(' in line[idx_eq:]:
                        # insert raw
                        if line[idx_eq+1] == ' ':
                            lines[i] = line[:idx_eq+2] + 'raw ' + line[idx_eq+2:]
                        else:
                            lines[i] = line[:idx_eq+1] + ' raw ' + line[idx_eq+1:]
                        print(f"Fixed {path}:{i+1} ({var_name})")

for path, lines in files_cache.items():
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')

