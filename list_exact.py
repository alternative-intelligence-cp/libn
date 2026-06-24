import os
import subprocess
import re

npkc = '/home/randy/Workspace/REPOS/nitpick/build/npkc'
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk') and file != 'all.npk':
            path = os.path.join(root, file)
            res = subprocess.run([npkc, path], capture_output=True, text=True)
            clean_out = ansi_escape.sub('', res.stdout + res.stderr)
            
            for line in clean_out.split('\n'):
                if 'error:' in line:
                    m = re.search(r'Line (\d+), Column \d+: (.*)', line)
                    if m:
                        line_num = int(m.group(1))
                        msg = m.group(2).strip()
                        print(f"{path}:{line_num}: {msg}")
