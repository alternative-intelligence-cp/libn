import re
import sys
import subprocess

def run_build():
    print("Building...")
    result = subprocess.run(["/home/randy/Workspace/REPOS/nitpick/build/npkc", "test_root.npk"], capture_output=True, text=True)
    # Filter out color codes
    log = re.sub(r'\x1b\[[0-9;]*m', '', result.stderr + "\n" + result.stdout)
    with open("build.log", "w") as f:
        f.write(log)
    return log

def map_errors(log_lines):
    # Same mapping logic
    files = []
    import os
    for root, _, filenames in os.walk('src'):
        for filename in filenames:
            if filename.endswith('.npk'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    lines = f.read().splitlines()
                    files.append({'path': filepath, 'lines': lines})

    error_pattern = re.compile(r'error: Line (\d+), Column (\d+): (.*)')
    
    mapped = []
    for line in log_lines:
        match = error_pattern.search(line)
        if match:
            line_num = int(match.group(1))
            col_num = int(match.group(2))
            msg = match.group(3)
            
            candidates = []
            for f in files:
                if len(f['lines']) >= line_num:
                    target_line = f['lines'][line_num - 1]
                    if "Unused result value" in msg:
                        candidates.append((f['path'], target_line))
                    elif "Cannot silently unwrap" in msg:
                        if "=" in target_line:
                            candidates.append((f['path'], target_line))
                    elif "Cannot assign value of type" in msg:
                        if "=" in target_line:
                            candidates.append((f['path'], target_line))
                    elif "Undefined identifier" in msg:
                        ident = re.search(r"Undefined identifier: '([^']+)'", msg)
                        if ident and ident.group(1) in target_line:
                            candidates.append((f['path'], target_line))
            if len(candidates) == 1:
                mapped.append({
                    'line': line_num,
                    'col': col_num,
                    'msg': msg,
                    'path': candidates[0][0],
                    'text': candidates[0][1]
                })
    return mapped

def apply_fixes():
    log = run_build()
    errors = map_errors(log.splitlines())
    
    fixes_made = 0
    # Process files
    file_edits = {}
    
    for err in errors:
        path = err['path']
        line_idx = err['line'] - 1
        text = err['text']
        col_idx = err['col'] - 1
        msg = err['msg']
        
        if path not in file_edits:
            with open(path, 'r') as f:
                file_edits[path] = f.read().splitlines()
        
        current_text = file_edits[path][line_idx]
        
        if "Unused result value" in msg:
            # Add drop(...)
            if " drop " not in current_text and "raw " not in current_text:
                # Find the start of the function call (at col_idx)
                # It might be indented
                prefix = current_text[:col_idx]
                suffix = current_text[col_idx:]
                file_edits[path][line_idx] = prefix + "drop " + suffix
                fixes_made += 1
                
        elif "Cannot silently unwrap" in msg or "Cannot assign value of type 'Result" in msg:
            # We need to insert 'raw ' after the '=' sign.
            if "=" in current_text and "raw " not in current_text:
                parts = current_text.split("=", 1)
                file_edits[path][line_idx] = parts[0] + "= raw " + parts[1].lstrip()
                fixes_made += 1

    for path, lines in file_edits.items():
        with open(path, 'w') as f:
            f.write("\n".join(lines) + "\n")
            
    return fixes_made

while True:
    fixes = apply_fixes()
    print(f"Applied {fixes} fixes.")
    if fixes == 0:
        break

