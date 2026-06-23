import os
import re
import subprocess

src_dir = "/home/randy/Workspace/REPOS/libn/src"
compiler = "/home/randy/Workspace/REPOS/nitpick/build/npkc"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

while True:
    changed = 0
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".npk"):
                path = os.path.join(root, file)
                res = subprocess.run([compiler, path], capture_output=True, text=True)
                output = ansi_escape.sub('', res.stdout + res.stderr)
                
                errors = []
                for line in output.split('\n'):
                    m = re.search(r'Line (\d+), Column \d+: Cannot silently unwrap', line)
                    if m:
                        errors.append(int(m.group(1)))
                
                if errors:
                    with open(path, 'r') as f:
                        lines = f.readlines()
                    
                    errors = sorted(list(set(errors)))
                    file_changed = False
                    for line_num in errors:
                        idx = line_num - 1
                        if idx < len(lines):
                            line_str = lines[idx]
                            if "raw " not in line_str:
                                new_line = re.sub(r'(=\s*|pass\s+|if\s*\(?|while\s*\(?|return\s+)([a-zA-Z_]\w*\s*\()', r'\1raw \2', line_str, count=1)
                                if new_line != line_str:
                                    lines[idx] = new_line
                                    file_changed = True
                    
                    if file_changed:
                        with open(path, 'w') as f:
                            f.writelines(lines)
                        print(f"Fixed {len(errors)} unwraps in {path}")
                        changed += 1
    print(f"Loop finished, changed {changed} files.")
    if changed == 0:
        break
