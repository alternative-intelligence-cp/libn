import os
import re

def parse_expr_backward(s, start_idx):
    idx = start_idx
    while idx > 0 and s[idx-1].isspace():
        idx -= 1
        
    if idx == 0: return 0
    
    if s[idx-1] == ')':
        paren_count = 1
        idx -= 1
        while idx > 0 and paren_count > 0:
            idx -= 1
            if s[idx] == ')': paren_count += 1
            elif s[idx] == '(': paren_count -= 1
        # also include any func name before `(`
        while idx > 0 and (s[idx-1].isalnum() or s[idx-1] in '_'):
            idx -= 1
    elif s[idx-1] == ']':
        paren_count = 1
        idx -= 1
        while idx > 0 and paren_count > 0:
            idx -= 1
            if s[idx] == ']': paren_count += 1
            elif s[idx] == '[': paren_count -= 1
        while idx > 0 and (s[idx-1].isalnum() or s[idx-1] in '_@&.'):
            idx -= 1
    elif s[idx-1] == '"':
        idx -= 1
        while idx > 0 and s[idx-1] != '"':
            idx -= 1
        idx -= 1 # consume opening quote
    else:
        while idx > 0 and (s[idx-1].isalnum() or s[idx-1] in '_@&.'):
            idx -= 1
            
    return idx

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    out = []
    in_struct = False
    
    for i, line in enumerate(lines):
        # Strip comment from processing, but keep it to append later
        comment_idx = line.find('//')
        if comment_idx != -1:
            # wait, what if `//` is inside a string? Libn doesn't really have `//` in strings.
            comment_part = line[comment_idx:]
            code_part = line[:comment_idx]
        else:
            comment_part = ''
            code_part = line
            
        if not code_part.strip() and comment_part:
            out.append(line)
            continue

        # 1. Struct defs
        if re.search(r'\bstruct\s+([a-zA-Z0-9_]+)\s*\{', code_part):
            code_part = re.sub(r'\bstruct\s+([a-zA-Z0-9_]+)\s*\{', r'struct:\1 = {', code_part)
            in_struct = True
            
        if in_struct and code_part.strip() == '}':
            code_part = code_part.replace('}', '};')
            in_struct = False
            
        # Top-level functions end with `};`
        # Functions are at indentation 0 and end with `}`
        if not in_struct and code_part == '}':
            code_part = '};'

        # 2. Pointer types `*Type` -> `Type->`
        # ONLY if followed by `:`
        code_part = re.sub(r'(?<=[\s\(\,])\*([a-zA-Z_][a-zA-Z0-9_]*):', r'\1->:', code_part)
        code_part = re.sub(r'^\*([a-zA-Z_][a-zA-Z0-9_]*):', r'\1->:', code_part)

        # 3. Casts: `as *Type` -> `as Type->`
        code_part = re.sub(r'as\s+\*([a-zA-Z_][a-zA-Z0-9_]*)', r'as \1->', code_part)

        # 4. Casts: `expr as Type` -> `@cast_unchecked<Type>(expr)`
        while ' as ' in code_part:
            idx = code_part.rfind(' as ')
            type_str_match = re.match(r'([a-zA-Z0-9_]+(->)?)', code_part[idx+4:])
            if not type_str_match:
                break
            type_str = type_str_match.group(1)
            
            expr_start = parse_expr_backward(code_part, idx)
            expr = code_part[expr_start:idx].strip()
            
            # replace
            code_part = code_part[:expr_start] + f"@cast_unchecked<{type_str}>({expr})" + code_part[idx+4+len(type_str):]

        # 5. Address-of `&` -> `@`
        code_part = re.sub(r'(?<![a-zA-Z0-9_\)\]])&([a-zA-Z_@])', r'@\1', code_part)

        # 6. Ternary
        if ' ? ' in code_part and ' : ' in code_part:
            m = re.search(r'([a-zA-Z0-9_\.\s\(\)!=<>\[\]\-]+)\s+\?\s+([a-zA-Z0-9_@]+)\s+:\s+([a-zA-Z0-9_@]+)', code_part)
            if m:
                cond = m.group(1).strip()
                a = m.group(2)
                b = m.group(3)
                if not cond.startswith('('):
                    cond = f"({cond})"
                code_part = code_part[:m.start()] + f"is {cond} : {a} : {b}" + code_part[m.end():]

        # 7. Deref `*(ptr)` -> `(ptr)[0]`
        if code_part.lstrip().startswith('*('):
            code_part = code_part.replace('*(', '(', 1).replace(') =', ')[0] =', 1)

        # 8. if/while parens
        m = re.match(r'^(\s*)(if|while)\s+(.*)$', code_part)
        if m:
            indent = m.group(1)
            kwd = m.group(2)
            rest = m.group(3)
            if '{' in rest:
                brace_idx = rest.find('{')
                cond = rest[:brace_idx].strip()
                if cond and not (cond.startswith('(') and cond.endswith(')')):
                    code_part = f"{indent}{kwd} ({cond}) " + rest[brace_idx:]
                    
        if 'if first {' in code_part:
            code_part = code_part.replace('if first {', 'if (first) {')

        # 9. remove extern variables
        if code_part.strip().startswith('extern '):
            # just comment it out
            code_part = '// ' + code_part

        out.append(code_part + comment_part)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
