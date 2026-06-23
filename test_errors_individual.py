import os
import subprocess
import re

npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

total_errors = 0
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            res = subprocess.run([npkc, path], capture_output=True, text=True)
            clean_out = ansi_escape.sub('', res.stdout + res.stderr)
            
            c = clean_out.count('error:')
            if c > 0:
                print(f"{path}: {c}")
            total_errors += c

print(f"Total isolated errors: {total_errors}")
