import re
import os
import glob

def find_files():
    files = []
    for root, _, fnames in os.walk('src'):
        for fname in fnames:
            if fname.endswith('.npk'):
                files.append(os.path.join(root, fname))
    return files

with open('clean_errors.txt') as f:
    clean_lines = [l.strip() for l in f.readlines()]

files = find_files()
fixes = {}

for clean in clean_lines:
    if 'error:' not in clean: continue
    m = re.search(r'Line (\d+), Column \d+: (.*)', clean)
    if not m: continue
    
    line = int(m.group(1))
    msg = m.group(2).strip()
    
    for file in files:
        with open(file, 'r') as f:
            flines = f.readlines()
        
        if line <= len(flines):
            orig = flines[line-1]
            new_val = orig
            
            if "Cannot silently unwrap Result" in msg:
                m_var = re.search(r"into '([^']+)'", msg)
                if m_var:
                    var_name = m_var.group(1)
                    if var_name in orig and '=' in orig and 'raw' not in orig and 'func:' not in orig:
                        # Protect against Result<T>:var = func()
                        lhs = orig.split('=')[0]
                        if "Result<" not in lhs:
                            new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)
            
            elif "while condition must be 'bool' type, got 'Result<bool>'" in msg or \
                 "Logical operator requires 'bool' type on right side, got 'Result<bool>'" in msg or \
                 "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg:
                if '!' in orig:
                    new_val = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', orig)
            
            elif "Unused result from NIL-returning function" in msg:
                if orig.strip().endswith(';') and 'drop' not in orig and '=' not in orig and 'pass ' not in orig and 'fail ' not in orig and 'return ' not in orig and 'break;' not in orig and 'continue;' not in orig:
                    new_val = re.sub(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\(.*?\));', r'\1drop(\2);', orig)

            elif "Cannot assign value of type 'Result<int64>' to variable of type 'int64'" in msg:
                if '=' in orig and not 'raw' in orig and 'func:' not in orig:
                    lhs = orig.split('=')[0]
                    if "Result<" not in lhs:
                        new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)

            if new_val != orig:
                if file not in fixes: fixes[file] = []
                if not any(f[0] == line for f in fixes[file]):
                    fixes[file].append((line, orig, new_val))

for f, f_fixes in fixes.items():
    with open(f, 'r') as file:
        flines = file.readlines()
    for line_num, orig, new in f_fixes:
        flines[line_num - 1] = new
        print(f"Fixed {f}:{line_num}")
    with open(f, 'w') as file:
        file.writelines(flines)

