import os
import re
import subprocess

src_dir = "/home/randy/Workspace/REPOS/libn/src"
compiler = "/home/randy/Workspace/REPOS/nitpick/build/npkc"

# Strip ANSI
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

changed = 0

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            # Run compiler on this file
            res = subprocess.run([compiler, path], capture_output=True, text=True)
            output = ansi_escape.sub('', res.stdout + res.stderr)
            
            # Find unwrap errors
            errors = []
            for line in output.split('\n'):
                # Line 340, Column 9: Cannot silently unwrap
                m = re.search(r'Line (\d+), Column \d+: Cannot silently unwrap', line)
                if m:
                    errors.append(int(m.group(1)))
            
            if errors:
                with open(path, 'r') as f:
                    lines = f.readlines()
                
                # We need to sort and unique the errors just in case
                errors = sorted(list(set(errors)))
                
                file_changed = False
                for line_num in errors:
                    idx = line_num - 1
                    if idx < len(lines):
                        line_str = lines[idx]
                        
                        # Find the function call on this line
                        # We want to insert 'raw ' before it.
                        # Typical cases:
                        # x = func()  -> x = raw func()
                        # pass func() -> pass raw func()
                        # if func() -> if raw func()
                        # while func() -> while raw func()
                        # This simple regex looks for a word followed by (.
                        # We only replace the FIRST function call on the line assuming it's the culprit.
                        # If the line already has 'raw', don't add it.
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

print(f"Total files changed: {changed}")
