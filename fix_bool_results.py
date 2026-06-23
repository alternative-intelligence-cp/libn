import os
import re
import subprocess

src_dir = "/home/randy/Workspace/REPOS/libn/src"
compiler = "/home/randy/Workspace/REPOS/nitpick/build/npkc"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

changed = 0

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            res = subprocess.run([compiler, path], capture_output=True, text=True)
            output = ansi_escape.sub('', res.stdout + res.stderr)
            
            fixes = set()
            for line in output.split('\n'):
                # 1. Logical NOT requires 'bool' type, got 'Result<bool>'
                m1 = re.search(r'Line (\d+), Column \d+: Logical NOT requires \'bool\' type, got \'Result<bool>\'', line)
                if m1:
                    fixes.add(int(m1.group(1)))
                
                # 2. if condition must be 'bool' type, got 'Result<bool>'
                m2 = re.search(r'Line (\d+), Column \d+: if condition must be \'bool\' type, got \'Result<bool>\'', line)
                if m2:
                    fixes.add(int(m2.group(1)))

            if fixes:
                with open(path, 'r') as f:
                    lines = f.readlines()
                
                file_changed = False
                for line_num in sorted(list(fixes)):
                    idx = line_num - 1
                    if idx < len(lines):
                        line_str = lines[idx]
                        
                        # Add raw if not present
                        # We look for the first function call after ! or if(
                        if "raw " not in line_str:
                            new_line = re.sub(r'(!\s*|if\s*\(\s*)([a-zA-Z_]\w*\s*\()', r'\1raw \2', line_str, count=1)
                            if new_line != line_str:
                                lines[idx] = new_line
                                file_changed = True

                if file_changed:
                    with open(path, 'w') as f:
                        f.writelines(lines)
                    print(f"Fixed {len(fixes)} bool result unwraps in {path}")
                    changed += 1

print(f"Total files changed: {changed}")
