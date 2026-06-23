import re
import os

with open("mapped_errors.txt", "r") as f:
    lines = f.readlines()

# Group errors by file
file_edits = {}

for line in lines:
    if not line.startswith("src/"):
        continue
    # Parse: src/fs/path.npk:220:9: error: Message...
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
        
    # We apply edits line by line. To avoid column offset issues, we can just do string replacements on the line.
    for lnum, cnum, msg in errors:
        if lnum < 1 or lnum > len(file_lines):
            continue
            
        line_idx = lnum - 1
        line_str = file_lines[line_idx]
        
        if "Member access (.) requires struct" in msg:
            # The column is where the `.` is, or where the identifier is.
            # E.g. "fp.fd" -> replace `.fd` with `->fd`
            # Let's just blindly replace `\.` with `->` for the known variable name before it.
            # Or just replace `.` with `->` on that line, if there is only one `.`
            # Or better, replace `(fp|f|file|sv|sb|iter)\.` with `\1->`
            line_str = re.sub(r'\b(fp|f|file|sv|sb|iter|self|v|s|str|st|a|b)\.', r'\1->', line_str)
            file_lines[line_idx] = line_str
            
        elif "Cannot silently unwrap Result" in msg:
            # We need to add 'raw ' before the function call if it's unwrapping.
            # The line might look like: int64:len = str_strlen_safe(s);
            # We want: int64:len = raw str_strlen_safe(s);
            # Or if it's `pass sys1(...)` -> we need to NOT unwrap if the function changed?
            # Wait, if we stripped Result<T> from return types, the function now returns T.
            # So `Result<int64>:r = sys1(...)` is wrong! It should be `int64:r = sys1(...)`.
            pass

    with open(fpath, "w") as f:
        f.write('\n'.join(file_lines))

print("Pointer dot fixes applied based on mapped_errors.txt.")
