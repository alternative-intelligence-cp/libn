from collections import defaultdict
import re

with open("build_errors.txt", "r") as f:
    text = f.read()

errors = text.split("\n\n")
counts = defaultdict(int)
file_counts = defaultdict(int)

for err in errors:
    lines = err.strip().split('\n')
    if not lines or 'error:' not in lines[0]: continue
    
    match = re.search(r'in (/[^:]+): (.*)', lines[0])
    if match:
        file = match.group(1).split('/')[-1]
        msg = match.group(2)
        if "Parse error" in msg:
            msg = lines[1].strip() if len(lines) > 1 else "Parse error"
            
        file_counts[file] += 1
        counts[file + ": " + msg] += 1
    else:
        # Check second line
        if len(lines) > 1:
            counts["Unknown: " + lines[1].strip()] += 1

print("Errors by file:")
for k, v in sorted(file_counts.items(), key=lambda x: -x[1]):
    print(f"{k}: {v}")

print("\nTop 20 errors:")
for k, v in sorted(counts.items(), key=lambda x: -x[1])[:20]:
    print(f"{k}: {v}")
