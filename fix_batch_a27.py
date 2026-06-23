import os
import re
import subprocess

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Replace *Struct with Struct->
    # Match * followed by Capitalized words, replacing with Capitalized->
    # e.g., *StrView -> StrView->
    content = re.sub(r'\*([A-Z][a-zA-Z0-9_]*)', r'\1->', content)

    # 2. Replace byte with uint8
    content = re.sub(r'\bbyte\b', 'uint8', content)

    # 3. Add raw to indexing assignments (naive approach for primitive types, mainly uint8)
    # Match: uint8:c = p[i];
    # Replace: uint8:c = raw p[i];
    content = re.sub(r'\b(uint8|int8|int32|int64|uint32|uint64|bool):([a-zA-Z0-9_]+)\s*=\s*(?!raw )([a-zA-Z0-9_]+)\[([^\]]+)\];', r'\1:\2 = raw \3[\4];', content)

    # 4. Enforce exit using int32
    # Match: exit 1; or exit code; or exit 0i64;
    # We replace: exit X; -> exit @cast_unchecked<int32>(X);
    # Actually wait, `exit X;` where X is an expression. We can just use `exit @cast_unchecked<int32>(X);` to be absolutely sure.
    # Actually, simpler: if it's `exit 0i32;` do nothing. If `exit 1i64;`, change to `exit 1i32;`.
    content = re.sub(r'\bexit\s+([0-9]+)i64\s*;', r'exit \1i32;', content)
    content = re.sub(r'\bexit\s+([0-9]+)\s*;', r'exit \1i32;', content)
    content = re.sub(r'\bexit\s+([a-zA-Z0-9_]+)\s*;', r'exit @cast_unchecked<int32>(\1);', content)
    # Fix exit @cast_unchecked<int32>(@cast_unchecked<int32>(X)); if it happens
    content = content.replace('exit @cast_unchecked<int32>(@cast_unchecked<int32>', 'exit @cast_unchecked<int32>')

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('/home/randy/Workspace/REPOS/libn/src'):
    for f in files:
        if f.endswith('.npk'):
            process_file(os.path.join(root, f))

# Also run compilation to see remaining errors
res = subprocess.run(['python3', '/home/randy/Workspace/REPOS/libn/scratch/compile.py'], capture_output=True, text=True)
if res.returncode != 0:
    print("Compilation check failed, running npkc directly on all files to count errors...")
    res2 = subprocess.run("find /home/randy/Workspace/REPOS/libn/src -name '*.npk' | xargs -n 1 /home/randy/Workspace/REPOS/nitpick/build/npkc", shell=True, capture_output=True, text=True)
    errs = [line for line in res2.stderr.split('\n') if 'error:' in line]
    print(f"Total remaining errors: {len(errs)}")
    if errs:
        print("Sample errors:")
        for e in errs[:20]:
            print(e)
else:
    print("All files compiled successfully!")

