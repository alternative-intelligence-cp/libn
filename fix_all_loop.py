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
                
                fixes = {}
                for line in output.split('\n'):
                    # 1. Cannot silently unwrap
                    m0 = re.search(r'Line (\d+), Column \d+: Cannot silently unwrap', line)
                    if m0:
                        fixes[int(m0.group(1))] = ('unwrap',)
                    
                    # 2. Cannot initialize variable
                    m1 = re.search(r'Line (\d+), Column \d+: Cannot initialize variable \'(.*?)\' of type \'(.*?)\' with value of type \'(.*?)\'', line)
                    if m1:
                        fixes[int(m1.group(1))] = ('init', m1.group(2), m1.group(3), m1.group(4))
                    
                    # 3. Cannot assign value
                    m2 = re.search(r'Line (\d+), Column \d+: Cannot assign value of type \'(.*?)\' to variable of type \'(.*?)\'', line)
                    if m2:
                        fixes[int(m2.group(1))] = ('assign', m2.group(2), m2.group(3))
                
                if fixes:
                    with open(path, 'r') as f:
                        lines = f.readlines()
                    
                    file_changed = False
                    # sort reverse so line numbers don't shift (though we don't insert lines anyway)
                    for line_num in sorted(fixes.keys(), reverse=True):
                        idx = line_num - 1
                        if idx < len(lines):
                            line_str = lines[idx]
                            fix = fixes[line_num]
                            
                            if fix[0] == 'unwrap':
                                if "raw " not in line_str:
                                    new_line = re.sub(r'(=\s*|pass\s+|if\s*\(?|while\s*\(?|return\s+)([a-zA-Z_]\w*\s*\()', r'\1raw \2', line_str, count=1)
                                    if new_line != line_str:
                                        lines[idx] = new_line
                                        file_changed = True
                            elif fix[0] == 'init':
                                var_type = fix[2]
                                val_type = fix[3]
                                new_line = line_str.replace(f"{var_type}:", f"{val_type}:")
                                if new_line != line_str:
                                    lines[idx] = new_line
                                    file_changed = True
                            elif fix[0] == 'assign':
                                val_type = fix[1]
                                var_type = fix[2]
                                if val_type.startswith("Result<") and not val_type.startswith("Result<Result<") and "raw " not in line_str:
                                    new_line = re.sub(r'(=\s*)([a-zA-Z_]\w*\s*\()', r'\1raw \2', line_str, count=1)
                                    if new_line != line_str:
                                        lines[idx] = new_line
                                        file_changed = True
                    
                    if file_changed:
                        with open(path, 'w') as f:
                            f.writelines(lines)
                        print(f"Fixed {len(fixes)} errors in {path}")
                        changed += 1
    
    print(f"Loop finished, changed {changed} files.")
    if changed == 0:
        break
