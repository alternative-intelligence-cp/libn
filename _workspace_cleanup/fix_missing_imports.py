import os
import re

def insert_import(file_path, import_stmt):
    with open(file_path, 'r') as f:
        code = f.read()

    if import_stmt in code:
        return

    # Find the last `use` statement
    last_use_idx = code.rfind('use "')
    if last_use_idx == -1:
        return

    end_of_line = code.find('\n', last_use_idx)
    new_code = code[:end_of_line+1] + import_stmt + '\n' + code[end_of_line+1:]

    with open(file_path, 'w') as f:
        f.write(new_code)

insert_import('src/io/bio/tmpfile.npk', 'use "src/syscall/syscall_numbers.npk".*;')

# Fix string indexing globally
def fix_string_indexing(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    
    orig = code
    # We want to change @cast_unchecked<int64>(@var[0]) to @cast_unchecked<int64>(@var)
    # ONLY if var is declared as `string:var` or `fixed string:var`
    
    # Let's just find all `string:VAR` declarations
    string_vars = re.findall(r'string:([a-zA-Z0-9_]+)\s*=', code)
    for var in string_vars:
        code = code.replace(f'@{var}[0]', f'@{var}')
    
    if code != orig:
        with open(file_path, 'w') as f:
            f.write(code)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            fix_string_indexing(os.path.join(root, f))
