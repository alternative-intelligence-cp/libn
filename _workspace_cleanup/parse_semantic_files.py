import re
import collections

with open("build.log", "r") as f:
    text = f.read()

# E.g. "test_root.npk:0:0: error: Line 45, Column 12:   [src/io/bio/fchar.npk] Undefined identifier: 'mem_memcpy'"
matches = re.findall(r'error: Line \d+, Column \d+:\s+\[([^\]]+)\]\s+(.*)', text)

files = collections.defaultdict(list)
for filename, msg in matches:
    files[filename].append(msg)

for filename, errors in sorted(files.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n=== {filename} ({len(errors)} errors) ===")
    c = collections.Counter(errors)
    for msg, count in c.most_common(5):
        print(f"  {count}: {msg}")
