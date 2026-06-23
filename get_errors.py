import os
import subprocess

errors = []

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for f in files:
        if f.endswith('.npk'):
            filepath = os.path.join(root, f)
            res = subprocess.run(['/home/randy/Workspace/REPOS/nitpick/build/npkc', filepath], capture_output=True, text=True)
            for line in res.stderr.split('\n'):
                if 'error:' in line:
                    errors.append((filepath, line))

# Group by file
by_file = {}
for filepath, msg in errors:
    if filepath not in by_file:
        by_file[filepath] = []
    by_file[filepath].append(msg)

for filepath in sorted(by_file.keys()):
    print(f"{filepath}: {len(by_file[filepath])} errors")
    for msg in by_file[filepath][:5]:
        print(f"  - {msg}")

print(f"Total: {len(errors)} errors")
