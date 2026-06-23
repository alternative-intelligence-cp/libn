import re
import os

with open("mapped_errors.txt", "r") as f:
    lines = f.readlines()

file_edits = {}

for line in lines:
    if not line.startswith("src/"):
        continue
    match = re.match(r'([^:]+):(-?\d+):(-?\d+): error: (.*)', line)
    if not match:
        continue
    fpath, lnum, cnum, msg = match.groups()
    lnum = int(lnum)
    cnum = int(cnum)
    
    if fpath not in file_edits:
        file_edits[fpath] = []
        
    file_edits[fpath].append((lnum, cnum, msg))

for fpath, errors in file_edits.items():
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, "r") as f:
        file_lines = f.read().split('\n')
        
    edits_by_line = {}
    for lnum, cnum, msg in errors:
        if lnum not in edits_by_line:
            edits_by_line[lnum] = []
        edits_by_line[lnum].append((cnum, msg))
            
    for lnum, col_msgs in edits_by_line.items():
        if lnum < 1 or lnum > len(file_lines):
            continue
            
        line_idx = lnum - 1
        line_str = file_lines[line_idx]
        
        col_msgs.sort(key=lambda x: x[0], reverse=True)
        
        for cnum, msg in col_msgs:
            if "has no member 'err'" in msg:
                line_str = line_str.replace(".err", ".error")
            elif "Undefined identifier: 'errno_set'" in msg:
                line_str = line_str.replace("errno_set", "libn_errno_set")
            elif "Cannot silently unwrap Result" in msg:
                # Need to insert 'raw ' before the function call.
                # Example: Result<int64>:r = sys1(...) => wait, no.
                # Example: int64:n = sys1(...) => int64:n = raw sys1(...)
                # The column points to the start of the function call!
                # Wait, cnum is 1-indexed. Let's insert 'raw ' at cnum-1?
                # Actually, wait. It could be `pass sys1(...)` => `pass raw sys1(...)`
                # Let's just do a simple substitution if we can find the assignment or pass.
                # Since we know it's missing `raw `, we'll just let the compiler tell us the column.
                # Is cnum pointing to the function call name? Yes.
                idx = cnum - 1
                if idx >= 0 and idx < len(line_str):
                    line_str = line_str[:idx] + "raw " + line_str[idx:]
            elif "Unused result from NIL-returning function" in msg:
                # We need to wrap the call in drop(...)
                # The call starts at cnum-1.
                # We don't have a full AST parser, so wrapping might be tricky.
                # But it's usually `func(...);`
                # So we can do: line_str = line_str[:idx] + "drop(" + line_str[idx:-1] + ");"
                # Assuming the line ends with `;`
                idx = cnum - 1
                if idx >= 0 and idx < len(line_str) and line_str.endswith(";"):
                    # Find the last ; and replace with );
                    line_str = line_str[:idx] + "drop(" + line_str[idx:len(line_str)-1] + ");"
        
        file_lines[line_idx] = line_str

    with open(fpath, "w") as f:
        f.write('\n'.join(file_lines))

print("Other fixes applied.")
