import os

filepath = 'src/str/strcpy.npk'
with open(filepath, 'r') as f:
    code = f.read()

# Replace int64:end with int64:end_ptr, and pass end; with pass end_ptr;
code = code.replace('int64:end = dst + i;', 'int64:end_ptr = dst + i;')
code = code.replace('pass end;', 'pass end_ptr;')

with open(filepath, 'w') as f:
    f.write(code)
