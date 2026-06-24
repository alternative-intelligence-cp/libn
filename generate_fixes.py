import re

with open('clean_errors.txt') as f:
    clean_lines = [l.strip() for l in f.readlines()]

with open('errors_to_fix.txt') as f:
    blocks = f.read().split('--- Error: ')

error_map = {}
for block in blocks:
    if not block.strip(): continue
    lines = block.strip().split('\n')
    msg = lines[0]
    m = re.search(r'\(Line (\d+)\)', msg)
    if m:
        line_num = int(m.group(1))
        msg_clean = re.sub(r'\s*\(Line \d+\)\s*', '', msg).strip()
        candidates = []
        for l in lines[1:]:
            m2 = re.match(r'^\s*([a-zA-Z0-9_/\.]+):(\d+):\s*(.*)', l)
            if m2:
                candidates.append((m2.group(1), int(m2.group(2)), m2.group(3)))
        error_map[(line_num, msg_clean)] = candidates

fixes = {}

for clean in clean_lines:
    if 'error:' not in clean: continue
    m = re.search(r'Line (\d+), Column \d+: (.*)', clean)
    if m:
        line = int(m.group(1))
        msg = m.group(2).strip()
        
        found = False
        target_file = None
        target_content = None
        
        for (l, m_clean), cands in error_map.items():
            if l == line and m_clean in msg:
                if len(cands) == 1:
                    target_file = cands[0][0]
                    target_content = cands[0][2]
                found = True
                break
        
        if not found:
            for (l, m_clean), cands in error_map.items():
                if l == line:
                    if len(cands) == 1:
                        target_file = cands[0][0]
                        target_content = cands[0][2]
                    break

        if target_file and target_content:
            new_content = target_content
            
            if "Cannot silently unwrap Result" in msg:
                m_var = re.search(r"into '([^']+)'", msg)
                if m_var:
                    var_name = m_var.group(1)
                    if var_name in target_content and '=' in target_content and not 'raw' in target_content:
                        if 'func:' not in target_content: # Protect against func declarations
                            new_content = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', target_content)
            
            elif "while condition must be 'bool' type, got 'Result<bool>'" in msg or \
                 "Logical operator requires 'bool' type on right side, got 'Result<bool>'" in msg or \
                 "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg:
                if '!' in target_content:
                    new_content = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', target_content)
            
            elif "Unused result from NIL-returning function" in msg:
                if target_content.strip().endswith(';'):
                    new_content = re.sub(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\(.*?\));', r'\1drop(\2);', target_content)
                    if new_content == target_content:
                        new_content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\(.*?\));', r'drop(\1);', target_content)

            elif "Cannot assign value of type 'Result<int64>' to variable of type 'int64'" in msg:
                if '=' in target_content and not 'raw' in target_content:
                    if 'func:' not in target_content:
                        new_content = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', target_content)

            if new_content != target_content:
                if target_file not in fixes:
                    fixes[target_file] = []
                fixes[target_file].append((line, target_content, new_content))

for f, f_fixes in fixes.items():
    with open(f, 'r') as file:
        lines = file.readlines()
    
    modified = False
    for line_num, orig, new in f_fixes:
        if line_num <= len(lines):
            curr = lines[line_num - 1].strip()
            if curr == orig.strip() or orig.strip() in curr:
                # To be safe, just replace the exact substring in the line
                lines[line_num - 1] = lines[line_num - 1].replace(orig.strip(), new.strip())
                print(f"Fixed {f}:{line_num}")
                print(f"  - {orig.strip()}")
                print(f"  + {new.strip()}")
                modified = True
            else:
                print(f"Mismatch in {f}:{line_num}")
                print(f"  Expected: {orig.strip()}")
                print(f"  Found:    {curr}")
    
    if modified:
        with open(f, 'w') as file:
            file.writelines(lines)

