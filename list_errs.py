import re
with open('compiler_errors.txt') as f:
    errs = f.read()

files = set()
for m in re.finditer(r'Parse error in (.*?):', errs):
    files.add(m.group(1))

print("Files with parse errors:")
for f in files: print(f)
