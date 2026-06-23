import re

log_path = "/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/.system_generated/tasks/task-9262.log"

with open(log_path, "r") as f:
    log_content = f.read()

# Pattern for Nitpick errors:
# /path/to/file.npk:0:0: error: Line <num>, Column <col>: <message>
err_pattern = re.compile(r"(/home/randy/Workspace/REPOS/libn/src/[a-zA-Z0-9_./]+):0:0: error: Line ([0-9]+), Column [0-9]+: (.*)")

files_with_errors = {}
for match in err_pattern.finditer(log_content):
    path = match.group(1)
    line = int(match.group(2))
    msg = match.group(3)
    if path not in files_with_errors:
        files_with_errors[path] = []
    files_with_errors[path].append((line, msg))

total = 0
for path in sorted(files_with_errors.keys()):
    count = len(files_with_errors[path])
    total += count
    print(f"{path}: {count} errors")
    # Print the first 3 unique errors
    msgs = list(set(msg for line, msg in files_with_errors[path]))
    for msg in msgs[:3]:
        print(f"  - {msg}")

print(f"Total: {total} errors")
