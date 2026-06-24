import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

# Just replace `return sys(..., a6);` and `return err_from_syscall(sys!!!(..., a6));`
# with `return sys!!(nr, a1, a2, a3, a4, a5, a6);` for all whitelist entries!
# Wait, let's just rewrite the entire pick block nicely.
import re

def replace_pick_block(match):
    lines = match.group(0).split('\n')
    new_lines = []
    for line in lines:
        if '(SYS_' in line:
            # extract the SYS_ name
            m = re.search(r'\(SYS_[A-Z0-9_]+\)', line)
            if m:
                sys_name = m.group(0)
                new_lines.append(f"        {sys_name} {{ return sys!!(nr, a1, a2, a3, a4, a5, a6); }},")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

content = re.sub(r'pick \(nr\) \{.*?\};\n', replace_pick_block, content, flags=re.DOTALL)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)
