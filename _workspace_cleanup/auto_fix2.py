import re
import os
import subprocess

def run_build():
    result = subprocess.run(["/home/randy/Workspace/REPOS/nitpick/build/npkc", "test_root.npk"], capture_output=True, text=True)
    log = re.sub(r'\x1b\[[0-9;]*m', '', result.stderr + "\n" + result.stdout)
    return log

def fix_all():
    log = run_build()
    
    # 1. Extract variables that failed to unwrap
    unwrap_vars = set()
    unwrap_pattern = re.compile(r"Cannot silently unwrap Result<[^>]+> into '([a-zA-Z0-9_]+)'")
    for match in unwrap_pattern.finditer(log):
        unwrap_vars.add(match.group(1))
        
    assign_pattern = re.compile(r"Cannot assign value of type 'Result<[^>]+>' to variable of type '[^']+'")
    # 2. Find lines that have `var = func(...)` and fix them
    
    # Unused results are harder because the variable name isn't given.
    # But wait! We can look at `mapped_errors.txt` or just use a generic regex for function calls on their own line.
    
    files = []
    for root, _, filenames in os.walk('src'):
        for filename in filenames:
            if filename.endswith('.npk'):
                files.append(os.path.join(root, filename))
                
    fixes = 0
    for fpath in files:
        with open(fpath, 'r') as f:
            lines = f.read().splitlines()
            
        changed = False
        for i in range(len(lines)):
            line = lines[i]
            
            # Fix unwrap variables
            for var in unwrap_vars:
                # int64:var = func(...)
                pattern = r"(\b" + var + r"\s*=\s*)([a-zA-Z0-9_]+)\("
                if re.search(pattern, line) and " raw " not in line and " drop " not in line:
                    lines[i] = re.sub(pattern, r"\1raw \2(", line)
                    changed = True
                    fixes += 1
            
            # Fix Result assignment (no variable name given in error, but we can guess it's an assignment)
            if re.search(r"^\s*(int64|bool|uint8|byte)\[?\]?(->)?\s*:\s*[a-zA-Z0-9_]+\s*=\s*[a-zA-Z0-9_]+\(", line):
                if " raw " not in line and " sys(" not in line:
                    # we don't know if this one failed, but maybe we can just make it raw if it failed.
                    pass
                    
            # Fix unused result
            # Matches:   func_name(...);
            if re.match(r"^\s*[a-zA-Z0-9_]+\([^;]*\);$", line):
                if not any(k in line for k in ["pass ", "fail ", "continue;", "break;", "drop ", "raw "]):
                    lines[i] = re.sub(r"^(\s*)([a-zA-Z0-9_]+\([^;]*\);)$", r"\1drop \2", line)
                    changed = True
                    fixes += 1

        if changed:
            with open(fpath, 'w') as f:
                f.write("\n".join(lines) + "\n")
                
    return fixes

while True:
    fixes = fix_all()
    print(f"Applied {fixes} fixes.")
    if fixes == 0:
        break
