import os
import subprocess
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

def compile_file(filepath):
    result = subprocess.run(["npkc", filepath], capture_output=True, text=True)
    # Strip ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', result.stderr + result.stdout)

def apply_fixes(filepath):
    output = compile_file(filepath)
    if "error: Line" not in output:
        return False
        
    lines = output.split('\n')
    
    with open(filepath, "r") as f:
        file_lines = f.readlines()
        
    changes_made = False
    
    # We apply fixes from bottom to top so that we don't mess up column indices!
    # Wait, column indices might change if we replace `.` with `->` (+1 char).
    # Line indices don't change if we don't add lines.
    
    # Parse errors
    errors = []
    for line in lines:
        match = re.search(r'Line (\d+), Column (\d+): (.*)', line)
        if match:
            l = int(match.group(1))
            c = int(match.group(2))
            msg = match.group(3)
            errors.append((l, c, msg))
            
    # Sort errors descending by line and column
    errors.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    for l, c, msg in errors:
        idx = l - 1
        if idx >= len(file_lines):
            continue
            
        orig_line = file_lines[idx]
        new_line = orig_line
        col = c - 1
        
        if "Member access (.) requires struct" in msg and "Use ->" in msg:
            # col points to the `.`.
            if col < len(new_line) and new_line[col] == '.':
                new_line = new_line[:col] + "->" + new_line[col+1:]
        elif "Undefined identifier:" in msg and "Did you mean" in msg:
            # e.g., Undefined identifier: 'r'. Did you mean 's'?
            m = re.search(r"Undefined identifier: '(.*?)'\. Did you mean '(.*?)'\?", msg)
            if m:
                old_id = m.group(1)
                new_id = m.group(2)
                # Ensure the identifier matches at col
                if new_line[col:col+len(old_id)] == old_id:
                    new_line = new_line[:col] + new_id + new_line[col+len(old_id):]
        
        if orig_line != new_line:
            file_lines[idx] = new_line
            changes_made = True

    if changes_made:
        with open(filepath, "w") as f:
            f.writelines(file_lines)
            
    return changes_made

def main():
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith(".npk"):
                path = os.path.join(root, f)
                while True:
                    if not apply_fixes(path):
                        break
    print("Auto-fix pass completed.")

if __name__ == "__main__":
    main()
