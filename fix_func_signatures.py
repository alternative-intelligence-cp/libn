import glob, re

for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        s = f.read()

    # Change func declarations: pub func:foo = Result<int64>(...) -> pub func:foo = int64(...)
    s = re.sub(r'func:(\w+)\s*=\s*Result<int64>\(', r'func:\1 = int64(', s)
    
    # Also fix Result<int8> or other types if they exist
    s = re.sub(r'func:(\w+)\s*=\s*Result<([a-zA-Z0-9_]+)>\(', r'func:\1 = \2(', s)

    # Change func:foo = void(...) -> func:foo = NIL(...)
    s = re.sub(r'func:(\w+)\s*=\s*void\(', r'func:\1 = NIL(', s)

    with open(filepath, 'w') as f:
        f.write(s)
