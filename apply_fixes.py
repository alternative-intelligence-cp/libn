import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_func = False
    brace_depth = 0

    for idx, line in enumerate(lines):
        orig_line = line
        line = line.rstrip('\n')
        
        # Split code and comment
        code_part = line
        comment_part = ""
        if '//' in line:
            parts = line.split('//', 1)
            code_part = parts[0]
            comment_part = '//' + parts[1]

        # 1. Arrays: int64:_atexit_handlers[32]; -> int64[32]:_atexit_handlers;
        code_part = re.sub(r'\b(stack\s+|global\s+|pub\s+|pub\s+global\s+|pub\s+stack\s+)?([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+)\s*\[([^\]]+)\]\s*;', r'\1\2[\4]:\3;', code_part)

        # 2. Pointers
        code_part = code_part.replace('*byte', 'uint8->')
        code_part = code_part.replace('*int64', 'int64->')
        code_part = code_part.replace('*uint64', 'uint64->')
        code_part = code_part.replace('*int32', 'int32->')
        code_part = code_part.replace('*uint32', 'uint32->')
        code_part = code_part.replace('*uint8', 'uint8->')
        code_part = code_part.replace('*int8', 'int8->')

        # 3. void -> NIL
        # Only whole words, avoid 'avoid' or similar
        code_part = re.sub(r'\bvoid\b', 'NIL', code_part)

        # 4. If / While parens
        # Safely wrap the condition if it's not already wrapped.
        # Match `if ... {` or `while ... {`
        m = re.match(r'^( *)((?:}\s*else\s+)?)(if|while)\s+(.*?)\s*\{\s*$', code_part)
        if m:
            indent = m.group(1)
            else_part = m.group(2)
            kw = m.group(3)
            cond = m.group(4).strip()
            
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
                code_part = f"{indent}{else_part}{kw} ({cond}) {{"
        
        # 5. Functions ending in `};`
        if code_part.strip().startswith('func:') or code_part.strip().startswith('pub func:'):
            in_func = True
            brace_depth = 0

        if in_func:
            brace_depth += code_part.count('{')
            brace_depth -= code_part.count('}')
            if brace_depth == 0 and code_part.strip() == '}':
                code_part = code_part.replace('}', '};')
                in_func = False

        # 6. `as` Casts
        # Match `(...) as type` first
        code_part = re.sub(r'\(([^)]+)\)\s+as\s+([a-zA-Z0-9_]+(?:->)?)', r'@cast_unchecked<\2>(\1)', code_part)
        # Match simple `var as type`
        code_part = re.sub(r'([a-zA-Z0-9_\.\[\]]+)\s+as\s+([a-zA-Z0-9_]+(?:->)?)', r'@cast_unchecked<\2>(\1)', code_part)

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
            
        # 7. Special exit.npk function call
        if 'call fn();' in line:
            indent = line[:len(line) - len(line.lstrip())]
            out.append(f"{indent}(NIL)():f = @cast_unchecked<(NIL)()>(fn);\n")
            out.append(f"{indent}f();\n")
            continue

        out.append(line + '\n')

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
