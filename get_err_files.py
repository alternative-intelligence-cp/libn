import re
with open('compiler_errors.txt', 'r') as f: lines = f.readlines()
cur = ""
for line in lines:
    line = re.sub(r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]', '', line).strip()
    if "Failed to parse module" in line:
        m = re.search(r"'(.*?)'", line)
        if m: cur = m.group(1)
    if "Line 153" in line and "Cannot silently unwrap" in line:
        print(f"File for Line 153: {cur}")
