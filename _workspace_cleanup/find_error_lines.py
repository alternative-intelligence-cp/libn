import os
import re

# Read the compiler output
with open('/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/tasks/task-12632.log', 'r') as f:
    log = f.read()

# Extract line numbers
lines_to_check = set()
for match in re.finditer(r'error: Line (\d+),', log):
    lines_to_check.add(int(match.group(1)))

# Scan all files
for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                lines = file.readlines()
                for line_num in lines_to_check:
                    if line_num <= len(lines):
                        line_content = lines[line_num - 1].strip()
                        # Only print if it looks somewhat suspicious or matches known bad patterns
                        if line_content:
                            # We can just print all non-empty matches and grep them later
                            print(f"{path}:{line_num}: {line_content}")
