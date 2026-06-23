import os
import re

with open("build_errors.txt", "r") as f:
    text = f.read()

# Strip ANSI
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_text = ansi_escape.sub('', text)

errors = []
for line in clean_text.split('\n'):
    m = re.search(r'Line (\d+), Column \d+: Cannot silently unwrap .* into \'(\w+)\'', line)
    if m:
        errors.append((int(m.group(1)), m.group(2)))

src_dir = "/home/randy/Workspace/REPOS/libn/src"

files_cache = {}
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                files_cache[path] = f.readlines()

changed_files = set()

for line_num, var_name in errors:
    idx = line_num - 1
    found = False
    for path, lines in files_cache.items():
        if idx < len(lines):
            # Check if this line contains the assignment to var_name
            line_str = lines[idx]
            if var_name in line_str and '=' in line_str:
                # Need to insert 'raw ' before the function call
                # Match `= func(...)`
                new_line = re.sub(r'=\s*([a-zA-Z_]\w*\s*\()', r'= raw \1', line_str)
                if new_line != line_str:
                    lines[idx] = new_line
                    changed_files.add(path)
                    found = True
                    break

for path in changed_files:
    with open(path, 'w') as f:
        f.writelines(files_cache[path])
    print(f"Fixed unwraps in {path}")
