import os
import subprocess
import re

npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

errors = []
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            res = subprocess.run([npkc, path], capture_output=True, text=True)
            clean_out = ansi_escape.sub('', res.stdout + res.stderr)
            
            for line in clean_out.splitlines():
                if "error:" in line:
                    errors.append(line)

print(f"Total errors: {len(errors)}")
if len(errors) > 0:
    for e in errors[:20]:
        print(e)
