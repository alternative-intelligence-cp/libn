import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    for line in lines:
        orig_line = line
        line = line.rstrip('\n')
        
        # Split code and comment
        code_part = line
        comment_part = ""
        if '//' in line:
            parts = line.split('//', 1)
            code_part = parts[0]
            comment_part = '//' + parts[1]

        # 4. If / While parens
        m = re.match(r'^( *)((?:}\s*else\s+)?)(if|while)\s+(.*?)\s*\{(.*)$', code_part)
        if m:
            indent = m.group(1)
            else_part = m.group(2)
            kw = m.group(3)
            cond = m.group(4).strip()
            rest = m.group(5)
            
            # Check if cond is fully wrapped in matching parens
            is_wrapped = False
            if cond.startswith('(') and cond.endswith(')'):
                depth = 0
                is_wrapped = True
                for i, c in enumerate(cond):
                    if c == '(': depth += 1
                    elif c == ')': depth -= 1
                    if depth == 0 and i < len(cond) - 1:
                        is_wrapped = False
                        break
            
            if not is_wrapped:
                code_part = f"{indent}{else_part}{kw} ({cond}) {{{rest}"
        
        # Re-attach comment
        if comment_part:
            if code_part.endswith('{'):
                line = code_part + '  ' + comment_part
            elif code_part == '':
                line = comment_part
            else:
                line = code_part + ' ' + comment_part
        else:
            line = code_part
            
        out.append(line + '\n')

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

