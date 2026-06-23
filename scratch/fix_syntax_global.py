import os
import glob
import re

src_dir = '/home/randy/Workspace/REPOS/libn/src'
npk_files = glob.glob(os.path.join(src_dir, '**', '*.npk'), recursive=True)

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add parens around `if` and `else if` conditions
    content = re.sub(r'\bif\s+(?!\()(.+?)\s*\{', r'if (\1) {', content)
    content = re.sub(r'else\s+if\s+(?!\()(.+?)\s*\{', r'else if (\1) {', content)
    
    # 2. Add parens around `while` conditions
    content = re.sub(r'\bwhile\s+(?!\()(.+?)\s*\{', r'while (\1) {', content)

    # 3. Replace 'is X ? Y : Z' with '(X) ? Y : Z'
    # 'is' requires parens if it isn't an 'is' operator. Wait, the error is "Expected '(' after 'is'".
    # Actually, the ternary in v0.12.x is `(cond) ? a : b` or `cond ? a : b`. `is` was removed for ternary!
    # Let's replace `is cond ? true : false` with `(cond) ? true : false`
    content = re.sub(r'\bis\s+(.+?)\s*\?', r'(\1) ?', content)
    
    # 4. Fix cast syntax: `expr as Type` -> `@cast_unchecked<Type>(expr)`
    # BUT we must be very careful not to match things weirdly.
    # We already did this with regex in some files.
    # Actually, we can skip `as` if we already did it or fix it manually if it fails.
    # Let's replace simple `as`:
    # `(\w+)\s+as\s+(\w+)` -> `@cast_unchecked<\2>(\1)`
    content = re.sub(r'\b([\w\.\_]+)\s+as\s+([\w\-\>\*]+)', r'@cast_unchecked<\2>(\1)', content)
    
    # Wait, what if it's `expr => Type`?
    content = re.sub(r'\b([\w\.\_]+)\s*=>\s*([\w\-\>\*]+)', r'@cast_unchecked<\2>(\1)', content)
    
    # 5. Replace `pass expr;` with `pass(expr);`
    content = re.sub(r'\bpass\s+(?!\()(.+?);', r'pass(\1);', content)

    # 6. Replace `fail expr;` with `fail(expr);`
    content = re.sub(r'\bfail\s+(?!\()(.+?);', r'fail(\1);', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

for f in npk_files:
    fix_file(f)
print("Syntax fixes applied globally.")
