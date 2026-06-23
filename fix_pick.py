import os
import re

def fix_pick_in_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # The issue:
    # 0i64 => pass 8i64;
    # 0i64 => { g_slab_freelist_0 = val; }
    # _ => pass 0i64;
    
    # We want to change lines like:
    #   VALUE => STATEMENT
    # to:
    #   (VALUE) { STATEMENT },
    # except the last one might not need a comma but it's fine if it has one.
    # and _ => STATEMENT to (*) { STATEMENT }

    def replacer(m):
        val = m.group(1).strip()
        stmt = m.group(2).strip()
        
        if val == '_':
            val_str = '(*)'
        else:
            val_str = f'({val})'
            
        if stmt.startswith('{') and stmt.endswith('}'):
            # Already has braces
            pass
        else:
            stmt = f'{{ {stmt} }}'
            
        return f'{val_str} {stmt},'

    # Regex to find: something => something_else
    # Let's match line by line inside pick blocks. Actually it's easier to just regex replace line by line
    new_lines = []
    in_pick = False
    for line in content.split('\n'):
        if 'pick' in line and '{' in line:
            in_pick = True
            new_lines.append(line)
            continue
        if in_pick and '}' in line and '=>' not in line:
            in_pick = False
            # remove the trailing comma from the last case if there is one
            if len(new_lines) > 0 and new_lines[-1].endswith(','):
                new_lines[-1] = new_lines[-1][:-1]
            new_lines.append(line)
            continue
            
        if in_pick and '=>' in line:
            # find "VAL => STMT"
            parts = line.split('=>', 1)
            val = parts[0].strip()
            stmt = parts[1].strip()
            
            if val == '_':
                val_str = '(*)'
            else:
                val_str = f'({val})'
                
            if stmt.startswith('{') and stmt.endswith('}'):
                # already has braces
                new_line = f'        {val_str} {stmt},'
            else:
                new_line = f'        {val_str} {{ {stmt} }},'
                
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    with open(path, 'w') as f:
        f.write('\n'.join(new_lines))

fix_pick_in_file('/home/randy/Workspace/REPOS/libn/src/mem/slab.npk')
fix_pick_in_file('/home/randy/Workspace/REPOS/libn/src/syscall/errno.npk')
print("Fixed pick syntax.")
