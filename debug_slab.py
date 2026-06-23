import subprocess
import re

res = subprocess.run(["/home/randy/Workspace/REPOS/nitpick/build/npkc", "src/mem/slab.npk"], capture_output=True, text=True)
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
output = ansi_escape.sub('', res.stdout + res.stderr)

errors = []
for line in output.split('\n'):
    m = re.search(r'Line (\d+), Column \d+: Cannot silently unwrap', line)
    if m:
        errors.append(int(m.group(1)))

print("Errors found:", errors)
