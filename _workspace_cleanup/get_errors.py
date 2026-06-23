import re
import collections

with open("build.log", "r") as f:
    lines = f.readlines()

files = collections.defaultdict(list)
for line in lines:
    if "error: Line" in line:
        match = re.search(r'\[([^\]]+)\]\s+(.*)', line)
        if match:
            filename = match.group(1)
            msg = match.group(2)
            files[filename].append(msg)

for filename, errors in sorted(files.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n=== {filename} ({len(errors)} errors) ===")
    error_counts = collections.Counter(errors)
    for msg, count in error_counts.most_common(5):
        print(f"  {count}: {msg}")

