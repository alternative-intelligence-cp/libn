import os
import re

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    out = []
    in_func = False
    brace_depth = 0

    for i, line in enumerate(lines):
        # Pointer types
        line = line.replace('*byte', 'uint8->')
        line = line.replace('*int64', 'int64->')
        line = line.replace('*uint64', 'uint64->')
        line = line.replace('*int32', 'int32->')
        line = line.replace('*uint32', 'uint32->')
        line = line.replace('*uint8', 'uint8->')
        line = line.replace('*int8', 'int8->')

        # Functions detection
        if line.strip().startswith('func:') or line.strip().startswith('pub func:'):
            in_func = True
            brace_depth = 0

        if in_func:
            brace_depth += line.count('{')
            brace_depth -= line.count('}')

            if brace_depth == 0 and line.strip() == '}':
                line = line.replace('}', '};')
                in_func = False

        # If / While
        m = re.match(r'^( *)((?:} else )?)(if|while)\s+(.*?)\s*\{\s*$', line)
        if m:
            indent = m.group(1)
            else_part = m.group(2)
            kw = m.group(3)
            cond = m.group(4).strip()
            if not (cond.startswith('(') and cond.endswith(')')):
                line = f"{indent}{else_part}{kw} ({cond}) {{\n"

        # Casts
        # x as y
        # Also handles pointer arithmetic cast: `(ptr - 16i64) as int64->`
        # Let's match `(...) as type` first
        line = re.sub(r'\(([^)]+)\)\s+as\s+([a-zA-Z0-9_]+(?:->)?)', r'@cast_unchecked<\2>(\1)', line)
        # Then match simple var as type
        line = re.sub(r'([a-zA-Z0-9_\.\[\]]+)\s+as\s+([a-zA-Z0-9_]+(?:->)?)', r'@cast_unchecked<\2>(\1)', line)

        out.append(line)

    with open(path, 'w') as f:
        f.writelines(out)

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            process_file(os.path.join(root, file))

