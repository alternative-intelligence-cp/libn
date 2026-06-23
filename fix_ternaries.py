import re
import glob
import os

def fix_ternaries():
    for file in glob.glob('src/**/*.npk', recursive=True):
        with open(file, 'r') as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            if ' ? ' in line and ':' in line and not line.strip().startswith('//'):
                # Match format: indent type:var = cond ? expr1 : expr2;
                m = re.match(r'^(\s*)([^=]+)=\s*(.+)\s*\?\s*(.+)\s*:\s*([^;]+);(.*)$', line)
                if m:
                    indent = m.group(1)
                    lvalue = m.group(2).strip()
                    cond = m.group(3).strip()
                    expr1 = m.group(4).strip()
                    expr2 = m.group(5).strip()
                    tail = m.group(6)
                    
                    new_lines.append(f"{indent}{lvalue} = {expr1};\n")
                    new_lines.append(f"{indent}if (!({cond})) {{ {lvalue.split(':')[-1] if ':' in lvalue else lvalue} = {expr2}; }}{tail}\n")
                    continue
            new_lines.append(line)
            
        with open(file, 'w') as f:
            f.writelines(new_lines)

fix_ternaries()
