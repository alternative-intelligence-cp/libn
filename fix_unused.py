import re
from collections import defaultdict

with open("build_errors.txt", "r") as f:
    text = f.read()

# Strip ANSI escape codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_text = ansi_escape.sub('', text)

fixes = defaultdict(list)

# Match: src/fs/path.npk:20:5: error: Unused result
err_pattern = re.compile(r'(src/[^:]+\.npk):(\d+):\d+: error: Unused result')

for line in clean_text.split('\n'):
    m = err_pattern.match(line)
    if m:
        filepath = m.group(1)
        linenum = int(m.group(2))
        fixes[filepath].append(linenum)

for filepath, lines in fixes.items():
    full_path = filepath
    with open(full_path, 'r') as f:
        file_lines = f.readlines()
    
    # Sort in reverse to modify from bottom to top (not really needed since we modify in place, but good practice if inserting lines)
    # Actually, we just modify the line directly.
    for l in set(lines):
        idx = l - 1
        line_str = file_lines[idx]
        
        # we want to prepend `drop ` before the function call.
        # Find the first non-whitespace character
        match = re.search(r'^(\s*)(.*)$', line_str)
        if match:
            indent = match.group(1)
            content = match.group(2)
            # Make sure we don't double drop
            if not content.startswith('drop '):
                file_lines[idx] = f"{indent}drop {content}\n"
    
    with open(full_path, 'w') as f:
        f.writelines(file_lines)
    print(f"Fixed {len(set(lines))} unused results in {filepath}")
