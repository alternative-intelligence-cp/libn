import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_decl = False
    brace_depth = 0

    seeking_brace = False

    for line in lines:
        if not in_decl and not seeking_brace:
            if re.match(r'^\s*(pub\s+)?(func|struct|trait):[a-zA-Z0-9_]+', line) or \
               re.match(r'^\s*(pub\s+)?struct\s+[a-zA-Z0-9_]+', line):
                seeking_brace = True
                if '{' in line:
                    seeking_brace = False
                    in_decl = True
                    brace_depth = line.count('{') - line.count('}')
            out.append(line)
        elif seeking_brace:
            if '{' in line:
                seeking_brace = False
                in_decl = True
                brace_depth = line.count('{') - line.count('}')
            out.append(line)
        else:
            brace_depth += line.count('{')
            brace_depth -= line.count('}')
            
            if brace_depth <= 0:
                in_decl = False
                # The line that brought brace_depth to <= 0 has the closing brace.
                # Find the last '}' and replace with '};'
                # Simple replacement for lines that end with } or } followed by whitespace
                if not '};' in line:
                    line = re.sub(r'\}\s*$', '};\n', line)
            out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))
