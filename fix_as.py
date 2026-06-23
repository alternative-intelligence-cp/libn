import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # We need to find `expr as Type` and replace with `@cast_unchecked<Type>(expr)`
    # This is a bit tricky with regex because `expr` might be complex.
    # Instead of full AST parsing, let's look for `as Type`.
    # A simple approach: 
    # For `(expr) as Type` -> `@cast_unchecked<Type>(expr)`
    # For `var as Type` -> `@cast_unchecked<Type>(var)`
    # For `func(...) as Type` -> `@cast_unchecked<Type>(func(...))`
    # Since `as` is a keyword, let's just do a manual string-level backwards search.
    
    out = []
    for line in content.split('\n'):
        while ' as ' in line:
            # find the last ' as ' in the line
            idx = line.rfind(' as ')
            type_str_match = re.match(r'([a-zA-Z0-9_]+(->)?)', line[idx+4:])
            if not type_str_match:
                break
            type_str = type_str_match.group(1)
            
            # Now find the expression before `as`.
            # We'll just read backwards, matching parenthesis if needed.
            expr_end = idx
            while expr_end > 0 and line[expr_end-1].isspace():
                expr_end -= 1
                
            expr_start = expr_end
            if expr_start > 0 and line[expr_start-1] == ')':
                # find matching '('
                paren_count = 1
                expr_start -= 1
                while expr_start > 0 and paren_count > 0:
                    expr_start -= 1
                    if line[expr_start] == ')':
                        paren_count += 1
                    elif line[expr_start] == '(':
                        paren_count -= 1
            elif expr_start > 0 and line[expr_start-1] == ']':
                # find matching '['
                paren_count = 1
                expr_start -= 1
                while expr_start > 0 and paren_count > 0:
                    expr_start -= 1
                    if line[expr_start] == ']':
                        paren_count += 1
                    elif line[expr_start] == '[':
                        paren_count -= 1
                # wait, if it's `a[b]`, we should also include `a`
                while expr_start > 0 and (line[expr_start-1].isalnum() or line[expr_start-1] in '_@'):
                    expr_start -= 1
            else:
                # read word backwards
                while expr_start > 0 and (line[expr_start-1].isalnum() or line[expr_start-1] in '_@().'):
                    expr_start -= 1
                    
            expr = line[expr_start:expr_end]
            # Replace
            new_line = line[:expr_start] + f"@cast_unchecked<{type_str}>({expr})" + line[idx+4+len(type_str):]
            line = new_line
            
        out.append(line)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

