import re

def rewrite_pick(path, var_name):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    out = []
    in_pick = False
    first_if = True

    for line in lines:
        if re.search(r'pick\s*\(?\s*' + var_name + r'\s*\)?\s*\{', line):
            in_pick = True
            first_if = True
            continue
        if in_pick:
            m = re.search(r'([a-zA-Z0-9_]+)\s*=>\s*pass\s+(.*);', line)
            if m:
                val = m.group(1)
                ret = m.group(2).strip()
                if val == '_':
                    out.append(f'        else {{ pass({ret}); }}\n')
                else:
                    prefix = 'if' if first_if else 'else if'
                    out.append(f'        {prefix} ({var_name} == {val}) {{ pass({ret}); }}\n')
                    first_if = False
                continue
            
            # For slab.npk where it's `=> { ... }` instead of `=> pass`
            m2 = re.search(r'([a-zA-Z0-9_]+)\s*=>\s*\{\s*(.*?)\s*\}', line)
            if m2:
                val = m2.group(1)
                body = m2.group(2).strip()
                if val == '_':
                    out.append(f'        else {{ {body} }}\n')
                else:
                    prefix = 'if' if first_if else 'else if'
                    out.append(f'        {prefix} ({var_name} == {val}) {{ {body} }}\n')
                    first_if = False
                continue

            if '}' in line and not re.search(r'\}', line.split('//')[0]).group() == False:
                # Naive check for end of pick block
                if line.strip() == '}':
                    in_pick = False
                    continue
            
            # If it's empty or comment, just append
            if line.strip() == '' or line.strip().startswith('//'):
                out.append(line)
                continue
            
            # fallback
            out.append(line)
        else:
            out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

rewrite_pick('src/syscall/errno.npk', 'e')
rewrite_pick('src/mem/slab.npk', 'i')
