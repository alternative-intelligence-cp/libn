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
                m2 = re.search(r'error: Logical operator requires(.*)', line)
                if m2:
                    pass
    return errors

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
            var_pattern = r'\b' + var_name + r'\b\s*='
            
            for f in npk_files:
                with open(f, 'r') as file:
                    lines = file.readlines()
                if line_num <= len(lines):
                    content = lines[line_num - 1]
                    if 'func:' not in content and re.search(var_pattern, content):
                        new_content = re.sub(r'(=\s*)([a-zA-Z_][a-zA-Z0-9_]*\()', r'\1raw \2', content)
                        # Avoid double raw
                        new_content = new_content.replace('raw raw ', 'raw ')
                        if new_content != content:
                            lines[line_num - 1] = new_content
                            with open(f, 'w') as file:
                                file.writelines(lines)
                            fixes_applied += 1
                            print(f"Fixed {var_name} unwrap in {f}:{line_num}")
                            break
            continue

        if "if condition must be 'bool' type, got 'Result<bool>'" in msg:
            for f in npk_files:
                with open(f, 'r') as file:
                    lines = file.readlines()
                if line_num <= len(lines):
                    content = lines[line_num - 1]
                    if 'if ' in content:
                        new_content = re.sub(r'if\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))\s*\)', r'if (raw \1 == true)', content)
                        new_content = new_content.replace('raw raw ', 'raw ')
                        if new_content != content:
                            lines[line_num - 1] = new_content
                            with open(f, 'w') as file:
                                file.writelines(lines)
                            fixes_applied += 1
                            print(f"Fixed if condition in {f}:{line_num}")
                            break
            continue
                    
        if "Logical NOT requires 'bool' type, got 'Result<bool>'" in msg:
            for f in npk_files:
                with open(f, 'r') as file:
                    lines = file.readlines()
                if line_num <= len(lines):
                    content = lines[line_num - 1]
                    if '!' in content:
                        new_content = re.sub(r'!\s*([a-zA-Z_][a-zA-Z0-9_]*\(.*?\))', r'(raw \1 == false)', content)
                        new_content = new_content.replace('raw raw ', 'raw ')
                        if new_content != content:
                            lines[line_num - 1] = new_content
                            with open(f, 'w') as file:
                                file.writelines(lines)
                            fixes_applied += 1
                            print(f"Fixed logical NOT in {f}:{line_num}")
                            break
            continue

        if "Cannot use Result<int64> as int64 in arithmetic" in msg or "Bitwise operators require same integer type on both sides. Got 'uint8' and 'bool'." in msg or "Bitwise operators require integer types" in msg:
            for f in npk_files:
                with open(f, 'r') as file:
                    lines = file.readlines()
                if line_num <= len(lines):
                    content = lines[line_num - 1]
                    # We will just greedily add raw to function calls that don't have it on this line
                    def repl(m):
                        if m.group(1).endswith('raw ') or m.group(1).endswith('func:'): return m.group(0)
                        # We also shouldn't prepend raw to control flow like if( or while(
                        kw = ['if', 'while', 'for', 'return', 'pass', 'fail']
                        if m.group(2)[:-1] in kw: return m.group(0)
                        return m.group(1) + 'raw ' + m.group(2)
                    
                    new_content = re.sub(r'(^|[^a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_]*\()', repl, content)
                    if new_content != content:
                        lines[line_num - 1] = new_content
                        with open(f, 'w') as file:
                            file.writelines(lines)
                        fixes_applied += 1
                        print(f"Fixed generic call in {f}:{line_num}")
                        break
            continue

    print(f"Applied {fixes_applied} fixes")
    return fixes_applied

if __name__ == '__main__':
    for _ in range(20):
        c = fix_errors()
        if c == 0:
            break
