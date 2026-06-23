import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # 1. Pointer Types: `*Type:var` -> `Type->:var`
    # Match `*Type` only if preceded by whitespace, `(`, `,`, or start of line, and followed by `:`
    # e.g., `    *FILE:f = fp as *FILE;` -> `    FILE->:f = fp as *FILE;`
    content = re.sub(r'(?<=[\s\(\,])\*([a-zA-Z_][a-zA-Z0-9_]*):', r'\1->:', content)
    # Also handle start of string
    content = re.sub(r'^\*([a-zA-Z_][a-zA-Z0-9_]*):', r'\1->:', content)

    # 2. Casts: `expr as Type` -> `@cast_unchecked<Type>(expr)`
    # Since `as *Type` becomes `@cast_unchecked<Type->>(...)`, we need to handle `as *Type` first!
    content = re.sub(r'as\s+\*([a-zA-Z_][a-zA-Z0-9_]*)', r'as \1->', content)

    # Now fix `as Type`. It's hard to use regex for arbitrary expr. 
    # But in libn, `expr` is usually simple: a var name, `&var`, `&var[0]`, `(expr + expr)`, `var.field`
    # Let's do string-based backwards parsing:
    lines = content.split('\n')
    out = []
    in_struct = False
    
    for i, line in enumerate(lines):
        # Struct start
        if re.search(r'\bstruct\s+([a-zA-Z0-9_]+)\s*\{', line):
            line = re.sub(r'\bstruct\s+([a-zA-Z0-9_]+)\s*\{', r'struct:\1 = {', line)
            in_struct = True
        elif in_struct and line.strip() == '}':
            line = line.replace('}', '};')
            in_struct = False

        # Fix `as Type` -> `@cast_unchecked<Type>(expr)`
        while ' as ' in line:
            idx = line.rfind(' as ')
            type_str_match = re.match(r'([a-zA-Z0-9_]+(->)?)', line[idx+4:])
            if not type_str_match:
                break
            type_str = type_str_match.group(1)
            
            # Read backwards
            expr_end = idx
            while expr_end > 0 and line[expr_end-1].isspace():
                expr_end -= 1
                
            expr_start = expr_end
            if expr_start > 0 and line[expr_start-1] == ')':
                paren_count = 1
                expr_start -= 1
                while expr_start > 0 and paren_count > 0:
                    expr_start -= 1
                    if line[expr_start] == ')': paren_count += 1
                    elif line[expr_start] == '(': paren_count -= 1
            elif expr_start > 0 and line[expr_start-1] == ']':
                paren_count = 1
                expr_start -= 1
                while expr_start > 0 and paren_count > 0:
                    expr_start -= 1
                    if line[expr_start] == ']': paren_count += 1
                    elif line[expr_start] == '[': paren_count -= 1
                while expr_start > 0 and (line[expr_start-1].isalnum() or line[expr_start-1] in '_@&'):
                    expr_start -= 1
            else:
                while expr_start > 0 and (line[expr_start-1].isalnum() or line[expr_start-1] in '_@&.'):
                    expr_start -= 1
            
            expr = line[expr_start:expr_end]
            # Replace
            line = line[:expr_start] + f"@cast_unchecked<{type_str}>({expr})" + line[idx+4+len(type_str):]
            
        # Address-of: `&var` -> `@var`
        # We only want to replace `&` when it's not preceded by a word char or `)` or `]`.
        # Wait! In bitwise AND it's preceded by space. Address of is usually `&name` or ` &name`.
        # `&` as bitwise AND has spaces on both sides: `a & b`.
        # Address-of is `&a`. So `&\w`
        # Let's replace `&` followed by alpha or `@` or `(` with `@` if preceded by space, `(`, `,`, `=`, `return`, `pass`, etc.
        # It's safer to just replace `&` that is followed immediately by a word char or `@` and NOT preceded by a word char.
        line = re.sub(r'(?<![a-zA-Z0-9_\)\]])&([a-zA-Z_@])', r'@\1', line)
        
        # Ternary operator: `cond ? true : false` -> `is (cond) : true : false`
        if ' ? ' in line and ' : ' in line:
            # simple regex since libn ternaries are basic
            # `var = cond ? a : b;` -> `var = is (cond) : a : b;`
            m = re.search(r'([a-zA-Z0-9_\.\s\(\)!=<>\[\]]+)\s+\?\s+([a-zA-Z0-9_]+)\s+:\s+([a-zA-Z0-9_]+)', line)
            if m:
                cond = m.group(1).strip()
                a = m.group(2)
                b = m.group(3)
                if not cond.startswith('('):
                    cond = f"({cond})"
                line = line[:m.start()] + f"is {cond} : {a} : {b}" + line[m.end():]
                
        # Dereference: `*(ptr)` -> `(ptr)[0]`
        # In libn, it's `*(@cast...` or similar. Let's just catch `*(...) =`
        # wait, `*(ptr)`:
        if line.lstrip().startswith('*('):
            line = line.replace('*(', '(', 1).replace(') =', ')[0] =', 1)

        # if/while parentheses
        m = re.match(r'^(\s*)(if|while)\s+(.*)$', line)
        if m:
            indent = m.group(1)
            kwd = m.group(2)
            rest = m.group(3)
            # if rest ends with `{`, we can check if it's wrapped.
            # but wait, it might not end with `{` on the same line!
            # let's just do a simple check for same-line `{`
            if '{' in rest:
                idx = rest.find('{')
                cond = rest[:idx].strip()
                if cond and not (cond.startswith('(') and cond.endswith(')')):
                    line = f"{indent}{kwd} ({cond}) " + rest[idx:]
        
        # also `if first {` across lines doesn't exist in libn? wait, in `fscanf.npk`:
        # `if (c < 0i64) { if first { pass FILE_EOF; } pass matched; }`
        if 'if first {' in line:
            line = line.replace('if first {', 'if (first) {')

        out.append(line)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
