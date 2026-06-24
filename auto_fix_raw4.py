import re
import os

def fix_errors():
    with open('errors_to_fix.txt', 'r') as f:
        content = f.read()

    errors = content.split('--- Error: ')
    applied = 0

    for err_block in errors:
        if not err_block.strip():
            continue
        
        lines = err_block.strip().split('\n')
        msg_line = lines[0]
        m = re.search(r'\(Line (\d+)\)', msg_line)
        if not m:
            continue
        line_num = int(m.group(1))

        # Check all candidate files
        candidates = []
        for l in lines[1:]:
            if ':' in l:
                # e.g. "  src/io/read.npk:155: if (r.value == 0i64) {"
                m2 = re.match(r'^\s*([a-zA-Z0-9_/\.]+):(\d+):\s*(.*)', l)
                if m2:
                    candidates.append((m2.group(1), m2.group(3)))

        for f, content in candidates:
            # Re-read file to apply replace
            with open(f, 'r') as file:
                file_lines = file.readlines()
            if line_num > len(file_lines):
                continue
            
            orig = file_lines[line_num - 1]
            new_val = orig

            if "Cannot silently unwrap Result" in msg_line:
                m_var = re.search(r"into '([^']+)'", msg_line)
                if m_var:
                    var_name = m_var.group(1)
                    if var_name in orig and '=' in orig:
                        new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)
            
            elif "while condition must be 'bool' type, got 'Result<bool>'" in msg_line or \
                 "Logical operator requires 'bool' type on right side, got 'Result<bool>'" in msg_line or \
                 "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg_line:
                if '!' in orig:
                    new_val = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', orig)
            
            elif "Unused result from NIL-returning function" in msg_line:
                # We need to wrap the function call in drop()
                # Find something like: func(args);
                new_val = re.sub(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\(.*?\));', r'\1drop(\2);', orig)
            
            elif "Cannot compare Result<uint8> to uint8 directly" in msg_line:
                # Already manually fixed strchr
                pass

            elif "Cannot assign value of type 'Result<int64>' to variable of type 'int64'" in msg_line:
                if '=' in orig and not 'raw' in orig:
                    new_val = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', orig)
            
            if new_val != orig:
                file_lines[line_num - 1] = new_val
                with open(f, 'w') as file:
                    file.writelines(file_lines)
                applied += 1
                print(f"Fixed {f}:{line_num} -> {new_val.strip()}")
                break # Only apply one fix per error block

    return applied

if __name__ == '__main__':
    fix_errors()

