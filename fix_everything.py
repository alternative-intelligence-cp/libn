import os
import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        content = fp.read()
        
    # 1. *byte to uint8->
    content = content.replace('*byte[]', 'uint8[]')
    content = content.replace('*byte', 'uint8->')
    
    # 2. Result wrappers in function signatures
    content = re.sub(r'(= \s*)Result<([a-zA-Z0-9_\*\[\]\->]+)>\s*\(', r'\1\2(', content)
    
    # 3. .err to .error
    content = re.sub(r'\.err\b', r'.error', content)
    
    # 4. errno_set to libn_errno_set
    content = re.sub(r'\berrno_set\(', r'libn_errno_set(', content)
    
    # 5. Pointer fields (. to ->)
    # Both bare and parenthesis-wrapped.
    # Parens: )\.len -> )->len
    content = re.sub(r'\)\.(len|capacity|end_idx|pos|fd|flags|state|err|error|eof|buf|data|ptr)\b', r')->\1', content)
    # Bare: sv.len -> sv->len
    content = re.sub(r'\b(sv|sb|iter|fp|f|file|s|str|v|a|b)\.(len|capacity|end_idx|pos|fd|flags|state|err|error|eof|buf|data|ptr)\b', r'\1->\2', content)

    # 6. sys wrappers raw
    # We remove 'raw ' from sys wrappers inside sys1, sys2, sys3 etc.
    # Or just replace `pass raw sys_safe(` with `pass sys_safe(`
    content = content.replace('pass raw sys_safe(', 'pass sys_safe(')
    content = content.replace('pass raw sys_full(', 'pass sys_full(')
    
    with open(file, 'w') as fp:
        fp.write(content)

print("Fixes applied.")
