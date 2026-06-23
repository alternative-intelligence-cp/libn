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
        
    # Apply from end of line to start of line to avoid column shifts!
    # So we group by line, sort by column descending
    edits_by_line = {}
    for lnum, cnum, msg in errors:
        if "Member access (.) requires struct" in msg:
            if lnum not in edits_by_line:
                edits_by_line[lnum] = []
            edits_by_line[lnum].append((cnum, msg))
            
    for lnum, col_msgs in edits_by_line.items():
        if lnum < 1 or lnum > len(file_lines):
            continue
            
        line_idx = lnum - 1
        line_str = file_lines[line_idx]
        
        # sort descending
        col_msgs.sort(key=lambda x: x[0], reverse=True)
        
        for cnum, msg in col_msgs:
            # cnum is 1-indexed. Sometimes the compiler reports the column of the identifier, not the dot itself.
            # e.g., if we have `sv.len`, the column might be the 's' or the '.'.
            # Let's search forward from cnum for the first '.'
            # Or backward if we are already past it.
            # Actually, `fp.fd` usually reports the column of the dot or the start.
            start_search = max(0, cnum - 5)
            dot_idx = line_str.find('.', start_search)
            if dot_idx != -1:
                line_str = line_str[:dot_idx] + '->' + line_str[dot_idx+1:]
        
        file_lines[line_idx] = line_str

    with open(fpath, "w") as f:
        f.write('\n'.join(file_lines))

print("Fixed dots by column.")
