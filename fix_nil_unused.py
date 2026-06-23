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
                m = re.search(r'Line (\d+), Column \d+: Unused result from NIL-returning function', line)
                if m:
                    fixes.add(int(m.group(1)))

            if fixes:
                with open(path, 'r') as f:
                    lines = f.readlines()
                
                file_changed = False
                for line_num in sorted(list(fixes)):
                    idx = line_num - 1
                    if idx < len(lines):
                        line_str = lines[idx]
                        
                        # Match a function call that occupies the whole line
                        # Typically: \s*func(...);
                        # We want to replace it with: \s*drop(func(...));
                        m = re.match(r'^(\s*)([a-zA-Z_]\w*\(.*\));\s*$', line_str)
                        if m:
                            new_line = f"{m.group(1)}drop({m.group(2)});\n"
                            if new_line != line_str:
                                lines[idx] = new_line
                                file_changed = True

                if file_changed:
                    with open(path, 'w') as f:
                        f.writelines(lines)
                    print(f"Fixed {len(fixes)} unused results in {path}")
                    changed += 1

print(f"Total files changed: {changed}")
