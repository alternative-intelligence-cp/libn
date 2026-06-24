import re
import os
import subprocess

def get_all_npk_files():
    files = []
    for root, _, fnames in os.walk('src'):
        for fname in fnames:
            if fname.endswith('.npk'):
                files.append(os.path.join(root, fname))
    return files

def run_compiler():
    if os.path.exists('build_errors.txt'):
        os.remove('build_errors.txt')
    subprocess.run(['/home/randy/Workspace/REPOS/nitpick/build/npkc', 'src/all.npk'], stdout=open('build_errors.txt', 'w'), stderr=subprocess.STDOUT)
    with open('build_errors.txt', 'r') as f:
        content = f.read()
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', content)

def parse_errors(output):
    errors = []
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
                pass
    return errors

def find_file_for_line(npk_files, line_num, check_func):
    for f in npk_files:
        with open(f, 'r') as file:
            lines = file.readlines()
            if line_num <= len(lines):
                if check_func(lines[line_num - 1]):
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
        
        # Pattern 1: Cannot silently unwrap into 'var_name'
        m_unwrap = re.search(r"Cannot silently unwrap Result<[^>]+> into '([^']+)'", msg)
        if m_unwrap:
            var_name = m_unwrap.group(1)
            # Find the file with an assignment to var_name at line_num
            # Avoid func declarations by checking it doesn't have 'func:'
            f, lines = find_file_for_line(npk_files, line_num, lambda l: 'func:' not in l and ('=' in l or 'pass' in l))
            if f:
                content = lines[line_num - 1]
                if var_name in content:
                    # Look for var_name = func(...) or var_name = @cast... func(...)
                    # A safe replacement: find the first function call after the equals sign
                    # and prepend 'raw ' to it, UNLESS it already has 'raw '.
                    new_content = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', content)
                    if new_content == content:
                        # Maybe there is a cast: = @cast<int64>(func(...))
                        # Or it's `pass func(...)` (but the error specifically says into 'var_name', so it's an assignment)
                        pass
                    
                    if new_content != content:
                        lines[line_num - 1] = new_content
                        with open(f, 'w') as file:
                            file.writelines(lines)
                        fixes_applied += 1
                        continue

        # Pattern 2: Cannot silently unwrap into return type
        m_return = re.search(r"Cannot silently unwrap Result<[^>]+> into return type", msg)
        if m_return:
            f, lines = find_file_for_line(npk_files, line_num, lambda l: 'pass ' in l)
            if f:
                content = lines[line_num - 1]
                new_content = re.sub(r'pass\s+([a-zA-Z_][a-zA-Z0-9_]*\()', r'pass raw \1', content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    continue
                    
        # Pattern 3: Bitwise operators require integer types ... got 'Result<int64>'
        if "Bitwise operators require integer types" in msg and "Result<" in msg:
            f, lines = find_file_for_line(npk_files, line_num, lambda l: ('|' in l or '&' in l or '^' in l or '<<' in l or '>>' in l))
            if f:
                content = lines[line_num - 1]
                # Try to wrap the function call in raw
                new_content = re.sub(r'([^a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_]*\()', r'\1raw \2', content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    continue
                    
        # Pattern 4: Cannot use Result<int64> as int64 in arithmetic
        if "Cannot use Result<int64> as int64 in arithmetic" in msg:
            f, lines = find_file_for_line(npk_files, line_num, lambda l: '+' in l or '-' in l or '*' in l or '/' in l or '%' in l)
            if f:
                content = lines[line_num - 1]
                # Replace any non-raw function call with raw. We just prepend raw to ANY word followed by ( that isn't raw.
                # Simplistic: look for func_name(
                def repl(m):
                    if m.group(1).endswith('raw '): return m.group(0)
                    return m.group(1) + 'raw ' + m.group(2)
                new_content = re.sub(r'(^|[^a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_]*\()', repl, content)
                if new_content != content:
                    lines[line_num - 1] = new_content
                    with open(f, 'w') as file:
                        file.writelines(lines)
                    fixes_applied += 1
                    continue

    print(f"Applied {fixes_applied} fixes")
    return fixes_applied

if __name__ == '__main__':
    for _ in range(20):
        c = fix_errors()
        if c == 0:
            break
