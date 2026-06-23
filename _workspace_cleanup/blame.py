import os
import re

errors = []
with open("build_errors11.txt", "r") as f:
    for line in f:
        if "error: Line " in line:
            m = re.search(r"Line (\d+), Column (\d+): (.*)", line)
            if m:
                errors.append({"line": int(m.group(1)), "col": int(m.group(2)), "msg": m.group(3)})

files = []
for root, _, fs in os.walk("src"):
    for f in fs:
        if f.endswith(".npk"):
            path = os.path.join(root, f)
            with open(path, "r") as fd:
                lines = fd.readlines()
                files.append((path, lines))

print(f"Found {len(errors)} errors")
for err in errors[:30]:
    line_no = err["line"]
    for path, lines in files:
        if line_no <= len(lines):
            # check if the error makes sense in this file
            l = lines[line_no-1].strip()
            # simple heuristic: if the column points to a keyword or identifier
            # or if it's very likely this file
            # Let's just print matching files where the line contains something related to the error
            if "msg" in err["msg"] and "msg" in l:
                print(f"Match: {path}:{line_no}: {l} -> {err['msg']}")
            elif "len" in err["msg"] and "len" in l:
                print(f"Match: {path}:{line_no}: {l} -> {err['msg']}")
            elif "ep" in err["msg"] and "ep" in l:
                print(f"Match: {path}:{line_no}: {l} -> {err['msg']}")
            elif "s" in err["msg"] and "s" in l:
                print(f"Match: {path}:{line_no}: {l} -> {err['msg']}")
            elif "string" in err["msg"] and '"' in l:
                print(f"Match: {path}:{line_no}: {l} -> {err['msg']}")
            elif "bool" in err["msg"]:
                print(f"Match bool: {path}:{line_no}: {l} -> {err['msg']}")
