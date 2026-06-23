with open('src/syscall/syscall.npk', 'r') as f:
    lines = f.readlines()

in_func = False
func_brace_level = 0

for i in range(len(lines)):
    line = lines[i]
    if line.startswith('pub func:') or line.startswith('func:'):
        in_func = True
        func_brace_level = 0
    
    if in_func:
        func_brace_level += line.count('{')
        func_brace_level -= line.count('}')
        
        # If we just closed the top-level func block
        if func_brace_level == 0 and '}' in line:
            # Add semicolon to the last '}'
            lines[i] = line.replace('}', '};', 1)
            in_func = False

with open('src/syscall/syscall.npk', 'w') as f:
    f.writelines(lines)
