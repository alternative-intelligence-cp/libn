import os
import subprocess
import re

npk_files = []
for root, _, files in os.walk("src"):
    for f in files:
        if f.endswith(".npk"):
            npk_files.append(os.path.join(root, f))

mapping = {}

for f in npk_files:
    with open(f, "r") as file:
        content = file.read()
    
    # inject syntax error at the very beginning
    with open(f, "w") as file:
        file.write("INVALID_TOKEN_MAP_LINES;\n" + content)
    
    # run compiler
    result = subprocess.run(["npkc", "test_root.npk"], capture_output=True, text=True)
    
    # find error
    m = re.search(r'error: Line (\d+),', result.stdout + result.stderr)
    if m:
        mapping[f] = int(m.group(1))
        
    # restore
    with open(f, "w") as file:
        file.write(content)

for k, v in sorted(mapping.items(), key=lambda x: x[1]):
    print(f"{v}: {k}")
