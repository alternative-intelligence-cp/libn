import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Fix struct declarations: `pub struct Name {` -> `pub struct:Name = {`
    content = re.sub(r'pub\s+struct\s+([a-zA-Z0-9_]+)\s*\{', r'pub struct:\1 = {', content)
    content = re.sub(r'struct\s+([a-zA-Z0-9_]+)\s*\{', r'struct:\1 = {', content)

    # Fix if and while missing parentheses.
    # We want to find `if ` or `while ` followed by a condition that is NOT in parentheses,
    # and ends with `{`. The condition can span multiple lines!
    # Because conditions can span lines, we use re.DOTALL or handle it manually.
    
    out = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # very simple heuristic for if / while
        m = re.match(r'^(\s*)(if|while)\s+(.*)$', line)
        if m:
            indent = m.group(1)
            kwd = m.group(2)
            rest = m.group(3)
            
            # if it already starts with `(`, it's probably fine
            # EXCEPT if it's `if (x == 1) && (y == 2) {`
            # To be safe, if the WHOLE condition is not inside ONE pair of (), we wrap it.
            
            # accumulate until we see `{` not inside a comment or string
            # Actually, let's just find the first `{` at the end of some line.
            cond_lines = [rest]
            j = i
            while '{' not in cond_lines[-1] and j + 1 < len(lines):
                j += 1
                cond_lines.append(lines[j])
                
            full_cond_text = '\n'.join(cond_lines)
            
            if '{' in full_cond_text:
                # split at the LAST `{` before any `//`?
                # Actually, simpler: find the first `{`
                idx = full_cond_text.find('{')
                cond_only = full_cond_text[:idx].strip()
                
                # Check if cond_only is wrapped in `(` `)`
                is_wrapped = False
                if cond_only.startswith('(') and cond_only.endswith(')'):
                    # verify it's a single group
                    depth = 0
                    valid = True
                    for k, char in enumerate(cond_only):
                        if char == '(': depth += 1
                        elif char == ')': depth -= 1
                        if depth == 0 and k < len(cond_only) - 1:
                            valid = False
                            break
                    is_wrapped = valid
                
                if not is_wrapped and cond_only != '':
                    # wrap it!
                    new_cond = f"({cond_only})"
                    new_full = f"{indent}{kwd} {new_cond} " + full_cond_text[idx:]
                    
                    # replace the lines
                    new_lines = new_full.split('\n')
                    lines[i:j+1] = new_lines
                    # don't increment i, process the new lines (though we just fixed it)
        i += 1

    with open(path, 'w') as f:
        f.write('\n'.join(lines))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

