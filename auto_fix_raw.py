import re
import os
import glob
import subprocess

def get_all_npk_files():
    files = []
    for root, _, fnames in os.walk('src'):
        for fname in fnames:
            if fname.endswith('.npk'):
                files.append(os.path.join(root, fname))
    return files

def run_compiler():
    # Remove old build_errors.txt
    if os.path.exists('build_errors.txt'):
        os.remove('build_errors.txt')
    subprocess.run(['/home/randy/Workspace/REPOS/nitpick/build/npkc', 'src/all.npk'], stdout=open('build_errors.txt', 'w'), stderr=subprocess.STDOUT)
    with open('build_errors.txt', 'r') as f:
        content = f.read()
    # Strip ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', content)

def parse_errors(output):
    errors = []
    # e.g. src/all.npk:0:0: error: Line 151, Column 5: Cannot silently unwrap Result<int64> into 'n' of type 'int64'
    for line in output.split('\n'):
        if line.startswith('src/all.npk:0:0: error:'):
            m = re.search(r'Line (\d+), Column (\d+): (.*)', line)
            if m:
                errors.append({
                    'line': int(m.group(1)),
                    'col': int(m.group(2)),
                    'msg': m.group(3)
                })
            else:
                m2 = re.search(r'error: Logical operator requires(.*)', line)
                if m2:
                    # In some cases the Line/Column is on the previous line or missing?
                    # Let's just catch what we can
                    pass
    return errors

def find_file_for_line(npk_files, line_num, check_func):
    for f in npk_files:
        with open(f, 'r') as file:
            lines = file.readlines()
            if line_num <= len(lines):
                line_content = lines[line_num - 1]
                if check_func(line_content):
                    return f, lines
    return None, None

def fix_errors():
    npk_files = get_all_npk_files()
    output = run_compiler()
    errors = parse_errors(output)
    
    fixes_applied = 0
    
    for err in errors:
        msg = err['msg']
        line_num = err['line']
        
        m_unwrap = re.search(r"Cannot silently unwrap Result<[^>]+> into '([^']+)'", msg)
        if m_unwrap:
            var_name = m_unwrap.group(1)
            f, lines = find_file_for_line(npk_files, line_num, lambda l: var_name in l and '=' in l)
            if f:
                content = lines[line_num - 1]
                # We need to insert 'raw ' before the function call.
                # Usually it looks like: int64:n = func(...)
                # We can do regex replace: = \s*([a-zA-Z_][a-zA-Z0-9_]*\() -> = raw \1
                new_content = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    print(f"Fixed unwrap in {f}:{line_num}")
                    continue
        
        if "if condition must be 'bool' type, got 'Result<bool>'" in msg:
            f, lines = find_file_for_line(npk_files, line_num, lambda l: 'if ' in l)
            if f:
                content = lines[line_num - 1]
                # Replace if (func(...)) with if (raw func(...) == true)
                new_content = re.sub(r'if\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))\s*\)', r'if (raw \1 == true)', content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    print(f"Fixed if condition in {f}:{line_num}")
                    continue
                    
        if "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg:
            f, lines = find_file_for_line(npk_files, line_num, lambda l: '!' in l)
            if f:
                content = lines[line_num - 1]
                new_content = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    print(f"Fixed logical NOT in {f}:{line_num}")
                    continue
                    
        # ... Other patterns can be added
        
    return fixes_applied

if __name__ == '__main__':
    for _ in range(10):
        c = fix_errors()
        if c == 0:
            break
