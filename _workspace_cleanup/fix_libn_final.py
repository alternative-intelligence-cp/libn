import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        code = f.read()

    orig_code = code

    # 1. Add semicolons after blocks (functions, structs)
    code = re.sub(r'(?m)^}$', r'};', code)

    # 2. Fix while / if parentheses
    # Matches lines like: "    if r.is_error {" or "        while remaining > 0i64 {"
    # We use a regex that looks for lines starting with whitespace, then if/while, then no '(', up to '{'
    code = re.sub(r'^(?P<indent>\s*)(?P<keyword>if|while)\s+(?!\()(?P<cond>[^{}\n]+?)\s*\{', r'\g<indent>\g<keyword> (\g<cond>) {', code, flags=re.MULTILINE)

    # Specific missing parenthesis in syscall.npk
    code = code.replace('if (prot & PROT_EXEC) != 0i64 {', 'if ((prot & PROT_EXEC) != 0i64) {')
    
    # 3. Fix Result<T> return types
    # This specifically targets ONLY the function definition signatures, not variables
    code = re.sub(r'(pub func:[A-Za-z0-9_]+\s*=\s*)Result<int64>(\([^)]*\)\s*\{)', r'\g<1>int64\g<2>', code)
    code = re.sub(r'(func:[A-Za-z0-9_]+\s*=\s*)Result<int64>(\([^)]*\)\s*\{)', r'\g<1>int64\g<2>', code)
    
    code = re.sub(r'(pub func:[A-Za-z0-9_]+\s*=\s*)Result<NIL>(\([^)]*\)\s*\{)', r'\g<1>NIL\g<2>', code)
    code = re.sub(r'(func:[A-Za-z0-9_]+\s*=\s*)Result<NIL>(\([^)]*\)\s*\{)', r'\g<1>NIL\g<2>', code)

    # 4. Fix void -> NIL
    code = re.sub(r'\bvoid\(', r'NIL(', code)
    code = re.sub(r'pass\s+void\s*;', r'pass NIL;', code)

    # 5. Fix r.err -> r.error
    code = code.replace('r.err', 'r.error')
    code = code.replace('ret.err', 'ret.error')
    
    # 6. Syscall / FFI tweaks
    code = code.replace('sys(', 'sys!!(')
    code = code.replace('fail ERR_BADARG as tbb8;', 'fail 22i32;')  # Use i32 for error codes

    # 7. specific pointer cast issues
    if 'wait.npk' in path:
        code = code.replace('&status, 0i64', '&status as int64, 0i64')
    if 'memutil.npk' in path:
        code = re.sub(r'@cast_unchecked<int64->>\(\(([a-zA-Z0-9_]+) \+ @cast_unchecked<int64->>\(([a-zA-Z0-9_]+)\)\)\);', r'@cast_unchecked<int64->>(\1 + \2);', code)
        code = code.replace('byte:tmp', 'uint8:tmp')
        code = code.replace('byte:target', 'uint8:target')
        code = code.replace('@cast_unchecked<byte>', '@cast_unchecked<uint8>')
        code = code.replace('byte:first', 'uint8:first')

    # 8. io module call corrections
    if 'read.npk' in path:
        code = code.replace('sys_read(', 'libn_read(')
    if 'write.npk' in path:
        code = code.replace('sys_write(', 'libn_write(')
    if 'file.npk' in path:
        code = code.replace('sys_read(SYS_READ, ', 'sys_safe(SYS_READ, ')
        code = code.replace('sys_write(SYS_WRITE, ', 'sys_safe(SYS_WRITE, ')

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed {path}")

def main():
    os.system('git checkout src/')
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
