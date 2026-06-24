import subprocess
import os
import re

def get_files():
    files = []
    for root, _, fnames in os.walk('src'):
        for fname in fnames:
            if fname.endswith('.npk') and fname != 'all.npk':
                files.append(os.path.join(root, fname))
    return files

files = get_files()
file_errors = {}

for f in files:
    res = subprocess.run(['/home/randy/Workspace/REPOS/nitpick/build/npkc', f], capture_output=True, text=True)
    out = res.stdout + res.stderr
    out = re.sub(r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]', '', out)
    lines = [l for l in out.split('\n') if l.startswith(f + ':0:0: error:')]
    if lines:
        file_errors[f] = lines

fixes = 0

for f, errors in file_errors.items():
    with open(f, 'r') as file:
        flines = file.readlines()
    
    modified = False
    for e in errors:
        m = re.search(r'Line (\d+), Column \d+: (.*)', e)
        if not m: continue
        line = int(m.group(1))
        msg = m.group(2)
        
        if line <= len(flines):
            orig = flines[line-1]
            new_val = orig
            
            if "Cannot silently unwrap Result" in msg:
                m_var = re.search(r"into '([^']+)'", msg)
                if m_var:
                    var_name = m_var.group(1)
                    if var_name in orig and '=' in orig and 'raw' not in orig and 'func:' not in orig:
                        new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)
            
            elif "while condition must be 'bool' type, got 'Result<bool>'" in msg or \
                 "Logical operator requires 'bool' type on right side, got 'Result<bool>'" in msg or \
                 "if condition must be 'bool' type, got 'Result<bool>'" in msg or \
                 "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg:
                if '!' in orig:
                    new_val = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', orig)
            
            elif "Unused result from NIL-returning function" in msg:
                if orig.strip().endswith(';') and 'drop' not in orig and '=' not in orig:
                    new_val = re.sub(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\(.*?\));', r'\1drop(\2);', orig)

            elif "Cannot assign value of type 'Result<int64>' to variable of type 'int64'" in msg:
                if '=' in orig and not 'raw' in orig and 'func:' not in orig:
                    new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)

            if new_val != orig:
                flines[line-1] = new_val
                modified = True
                print(f"Fixed {f}:{line} - {msg}")
                fixes += 1
    
    if modified:
        with open(f, 'w') as file:
            file.writelines(flines)

print(f"Total applied fixes: {fixes}")
