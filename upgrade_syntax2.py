import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_func = False
    brace_depth = 0

    for i, line in enumerate(lines):
        # 1. Strip trailing newline to make regex easier
        orig_line = line
        line = line.rstrip('\n')
        
        # We need to separate the code from the comment (if any)
        comment_part = ""
        code_part = line
        if '//' in line:
            parts = line.split('//', 1)
            code_part = parts[0]
            comment_part = '//' + parts[1]

        # If / While
        # We can just look for `if ` or `while ` or `else if `
        m = re.match(r'^( *)((?:}\s*else\s+)?)(if|while)\s+(.*?)\s*\{\s*$', code_part)
        if m:
            indent = m.group(1)
            else_part = m.group(2)
            kw = m.group(3)
            cond = m.group(4).strip()
            if not (cond.startswith('(') and cond.endswith(')')):
                code_part = f"{indent}{else_part}{kw} ({cond}) {{"
                
        # Re-attach comment
        if comment_part:
            if code_part.endswith('{'):
                line = code_part + '  ' + comment_part
            else:
                line = code_part + comment_part
        else:
            line = code_part
            
        line += '\n'
        out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

