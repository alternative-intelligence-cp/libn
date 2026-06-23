import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_struct = False
    brace_depth = 0

    for line in lines:
        if not in_struct:
            if re.match(r'^\s*(pub\s+)?struct:[a-zA-Z0-9_]+\s*=\s*\{', line):
                in_struct = True
                brace_depth = 1
                # count other braces on the line if any (unlikely for struct def)
            out.append(line)
        else:
            brace_depth += line.count('{')
            brace_depth -= line.count('}')
            
            if brace_depth == 0:
                in_struct = False
                # The line that brought brace_depth to 0 has the closing brace.
                # Replace '}' with '};' if not already
                if not '};' in line:
                    line = re.sub(r'\}\s*$', '};\n', line)
            out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
