import os
import re

def process_file(path):
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    out = []
    
    for line in lines:
        # Match `stack type:name[size];` OR `type:name[size];`
        # e.g., `int64:_atexit_handlers[32];` -> `int64[32]:_atexit_handlers;`
        # But wait! We need to make sure it doesn't match `struct:name {` or something.
        # So we match `^(\s*(?:stack\s+)?)([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\[([0-9a-zA-Z_\+\-\* ]+)\];`
        m = re.search(r'^(\s*(?:stack\s+|pub\s+|fixed\s+)?)([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\[([0-9a-zA-Z_\+\-\* ]+)\];', line)
        if m:
            prefix = m.group(1)
            t = m.group(2)
            name = m.group(3)
            size = m.group(4)
            line = f"{prefix}{t}[{size}]:{name};"
            
        # Match ternary operator: `var = cond ? a : b;`
        # Or `return cond ? a : b;` -> `pass is (cond) : a : b;`
        # We can just look for ` ? ` and ` : `
        if ' ? ' in line and ' : ' in line and not line.strip().startswith('//'):
            # simple replacement: split by `?` and `:`
            # `prefix cond ? true_expr : false_expr`
            idx_q = line.rfind(' ? ')
            idx_c = line.find(' : ', idx_q)
            if idx_q != -1 and idx_c != -1:
                cond_part = line[:idx_q]
                true_part = line[idx_q+3:idx_c]
                false_part = line[idx_c+3:]
                
                # We need to find where the condition starts. Usually it's after `=`, `pass`, or `return`.
                # Let's search backwards in cond_part for `=` or `pass ` or `return ` or `(`
                m_start = re.search(r'(=|pass |return |\()\s*', cond_part)
                if m_start:
                    start_idx = m_start.end()
                    prefix = cond_part[:start_idx]
                    cond = cond_part[start_idx:].strip()
                else:
                    # fallback, assume the whole line before `?` is cond? No, maybe it starts at the first non-whitespace
                    start_idx = len(cond_part) - len(cond_part.lstrip())
                    prefix = cond_part[:start_idx]
                    cond = cond_part[start_idx:].strip()
                    
                if not cond.startswith('('):
                    cond = f"({cond})"
                
                line = f"{prefix}is {cond} : {true_part} : {false_part}"
                
        out.append(line)

    with open(path, 'w') as f:
        f.write('\n'.join(out))

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))
