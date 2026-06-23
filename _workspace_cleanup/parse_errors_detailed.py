import collections
import re

with open("build.log", "r") as f:
    lines = f.readlines()

error_types = collections.defaultdict(int)
files = collections.defaultdict(int)

for i, line in enumerate(lines):
    if "error: " in line:
        # Example line: test_root.npk:0:0: error: Line 1, Column 1:   [/home/randy/Workspace/REPOS/libn/src/io/bio/tmpfile.npk] Failed to parse module
        # Wait, the semantic errors look different.
        # Example: src/io/bio/fchar.npk:45:20: error: Undefined identifier: 'r'
        match = re.search(r'([a-zA-Z0-9_./-]+):(\d+):(\d+):\s+error:\s+(.*)', line)
        if match:
            filename = match.group(1)
            msg = match.group(4).strip()
            # Generalize the message
            gen_msg = re.sub(r"'.*?'", "'...'", msg)
            error_types[gen_msg] += 1
            files[filename] += 1

print("--- Top Error Types ---")
for msg, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"{count}: {msg}")

print("\n--- Top Files with Errors ---")
for file, count in sorted(files.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"{count}: {file}")
