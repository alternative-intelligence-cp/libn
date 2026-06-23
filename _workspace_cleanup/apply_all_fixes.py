import os
import re

def process_file(path):
    with open(path, 'r') as f:
        code = f.read()
    orig = code

    # 1. Rewrite casts and pointers
    # C-style pointer declarations
    code = re.sub(r'(\w+)\*:\s*([a-zA-Z0-9_]+)', r'\1->:\2', code)
    code = re.sub(r'byte\s+', 'uint8 ', code)
    code = re.sub(r'byte\*', 'uint8->', code)
    code = re.sub(r'byte->', 'uint8->', code)
    
    # C-style casts
    def cast_replacer(m):
        type_str = m.group(1).strip()
        expr_str = m.group(2).strip()
        if '*' in type_str:
            type_str = type_str.replace('*', '->')
        if type_str == 'byte->':
            type_str = 'uint8->'
        return f"@cast_unchecked<{type_str}>({expr_str})"
    
    # Only match if the "type" is a known type to avoid comment corruption
    type_pattern = r'(int64|int32|int16|int8|uint64|uint32|uint16|uint8|byte|tbb8|void|NIL)(?:\s*\*|->)?'
    code = re.sub(r'\(\s*(' + type_pattern + r')\s*\)\s*\(\s*([^;]+)\s*\)', cast_replacer, code)
    code = re.sub(r'\(\s*(' + type_pattern + r')\s*\)\s*([a-zA-Z0-9_&\[\]]+)', cast_replacer, code)
    
    # "as" casts (like memset.npk)
    code = re.sub(r'\)\s*as\s+uint8', r') /* as uint8 removed, handle manually if needed */', code)
    # Actually, @cast_unchecked<uint8>(expr)
    code = re.sub(r'\(([^)]+)\)\s*as\s+uint8', r'@cast_unchecked<uint8>(\1)', code)
    
    # 2. Fix structs
    def struct_replacer(m):
        struct_name = m.group(1).strip()
        return f"struct:{struct_name} = {{"
    code = re.sub(r'struct\s+([a-zA-Z0-9_]+)\s*\{', struct_replacer, code)

    # 3. Fix if/else if parens (avoiding double parens)
    def is_fully_enclosed(s):
        if not s.startswith('(') or not s.endswith(')'):
            return False
        count = 0
        for i, char in enumerate(s):
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count == 0 and i < len(s) - 1:
                return False
        return count == 0

    def fix_else_if(m):
        cond = m.group(1).strip()
        if is_fully_enclosed(cond):
            return f"else if {cond} {{"
        return f"else if ({cond}) {{"
    code = re.sub(r'else\s+if\s+([^{}\n]+?)\s*\{', fix_else_if, code)

    def fix_if(m):
        cond = m.group(1).strip()
        if "f.buf_mode ==" in cond:
            print(f"DEBUG cond: '{cond}'")
            print(f"DEBUG is_fully_enclosed: {is_fully_enclosed(cond)}")
        if is_fully_enclosed(cond):
            return f"if {cond} {{"
        return f"if ({cond}) {{"
    code = re.sub(r'\bif\s+([^{}\n]+?)\s*\{', fix_if, code)

    def fix_while(m):
        cond = m.group(1).strip()
        if is_fully_enclosed(cond):
            return f"while {cond} {{"
        return f"while ({cond}) {{"
    code = re.sub(r'\bwhile\s+([^{}\n]+?)\s*\{', fix_while, code)



    # 4. Rename 'limit' to 'limit_val'
    code = re.sub(r'\blimit\b', 'limit_val', code)

    # 6. Fix specific missing parens in mmap.npk, memutil.npk, syscall.npk
    code = code.replace("if ((prot & PROT_EXEC) != 0i64) {", "if ((prot & PROT_EXEC) != 0i64) {") # idempotency
    code = code.replace("if (prot & PROT_EXEC) != 0i64) {", "if ((prot & PROT_EXEC) != 0i64) {")
    code = code.replace("if (raw has_zero_byte(v) {", "if (raw has_zero_byte(v)) {")
    code = code.replace("if (size > 0i64 && n > (9223372036854775807i64 / size) {", "if (size > 0i64 && n > (9223372036854775807i64 / size)) {")
    
    # 7. Remove volatile
    code = code.replace("volatile p[i]", "p[i]")

    if code != orig:
        with open(path, 'w') as f:
            f.write(code)

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
