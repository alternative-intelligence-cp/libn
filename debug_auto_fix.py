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
    return errors

def find_file_for_line(npk_files, line_num, check_func):
    for f in npk_files:
        with open(f, 'r') as file:
            lines = file.readlines()
            if line_num <= len(lines):
                if check_func(lines[line_num - 1]):
                    return f, lines
    return None, None

npk_files = get_all_npk_files()
output = run_compiler()
errors = parse_errors(output)

for err in errors[:5]:
    msg = err['msg']
    line_num = err['line']
    print(f"Checking line {line_num}: {msg}")
    
    m_unwrap = re.search(r"Cannot silently unwrap Result<[^>]+> into '([^']+)'", msg)
    if m_unwrap:
        var_name = m_unwrap.group(1)
        f, lines = find_file_for_line(npk_files, line_num, lambda l: 'func:' not in l and ('=' in l or 'pass' in l))
        if f:
            print(f"Found in {f}")
            content = lines[line_num - 1]
            print(f"Content: {content.strip()}")
            new_content = re.sub(r'=\s*([a-zA-Z_][a-zA-Z0-9_]*\()', r'= raw \1', content)
            print(f"New Content: {new_content.strip()}")
        else:
            print("Not found in any file")
