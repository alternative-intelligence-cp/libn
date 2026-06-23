import os, re

def process(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    new_content = content
    
    # Fix 1: as cast
    new_content = re.sub(r'\b([a-zA-Z0-9_.]+)\s+as\s+([a-zA-Z0-9_]+)\b', r'@cast_unchecked<\2>(\1)', new_content)
    
    # Fix 2: *Type:var = expr;
    new_content = re.sub(r'\*([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\s*=\s*([^\n;]+);', r'\1->:\2 = @cast_unchecked<\1->>(\3);', new_content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process(os.path.join(root, file))
