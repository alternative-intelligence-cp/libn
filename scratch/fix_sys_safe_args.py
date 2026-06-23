import os
import re

def fix_sys_safe_calls(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    modified = False
    for i in range(len(lines)):
        line = lines[i]
        # Look for sys_safe(...) 
        if 'sys_safe(' in line:
            # Find all a.b
            matches = re.findall(r'\b([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)\b', line)
            if matches:
                indent = line[:len(line) - len(line.lstrip())]
                pre_statements = []
                for obj, field in matches:
                    var_name = f"{obj}_{field}"
                    pre_statements.append(f"{indent}int64:{var_name} = {obj}.{field};\n")
                    # replace in line
                    line = re.sub(rf'\b{obj}\.{field}\b', var_name, line)
                
                # Replace line
                lines[i] = "".join(pre_statements) + line
                modified = True
                
    if modified:
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"Fixed {file_path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            fix_sys_safe_calls(os.path.join(root, file))
