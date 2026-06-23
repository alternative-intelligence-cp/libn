import os
import re

def rewrite_file(path):
    with open(path, 'r') as f:
        code = f.read()
    
    orig_code = code

    # 1. Fix *(expr) = val; -> (expr)[0] = val;
    # But wait, it could be `*(expr) = val;` or `*(expr) = val`
    code = re.sub(r'\*\(([^)]+)\)\s*=\s*([^;]+);', r'(\1)[0] = \2;', code)

    # 2. Fix pointer declarations: *Type:name -> Type->:name
    def fix_ptr_decl(m):
        typ = m.group(1)
        name = m.group(2)
        if typ == 'byte':
            typ = 'uint8'
        return f"{typ}->:{name}"
    
    code = re.sub(r'^\s*\*(int64|byte|uint8|FILE|void|StrView|StrViewIter|StrBuf)\s*:\s*([a-zA-Z0-9_]+)', r'    \g<1>->:\g<2>', code, flags=re.MULTILINE)

    # 3. Fix `as` casts
    def fix_cast(m):
        expr = m.group(1).strip()
        typ = m.group(2).strip()
        
        if typ.startswith('*'):
            typ = typ[1:] + '->'
        if typ == 'byte':
            typ = 'uint8'
        elif typ == 'byte->':
            typ = 'uint8->'
            
        return f"@cast_unchecked<{typ}>({expr})"

    # Loop until no more replacements (for nested casts like `(a as b) as c`)
    while True:
        new_code = re.sub(r'((?:\([^)]+\))|(?:&?[a-zA-Z0-9_]+(?:\[[^\]]+\])*(?:\.[a-zA-Z0-9_]+)*))\s+as\s+(\*?[a-zA-Z0-9_]+)', fix_cast, code)
        if new_code == code:
            break
        code = new_code

    # 4. Also replace `byte:` with `uint8:` in general for non-pointer decls
    code = re.sub(r'\bbyte:', 'uint8:', code)
    code = re.sub(r'\bbyte\b', 'uint8', code) # be careful with this, might match other things
    # Wait, 'byte' -> 'uint8' is generally safe for types in this codebase

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed casts in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                rewrite_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
