import re

filepath = "/home/randy/Workspace/REPOS/libn/src/syscall/errno.npk"
with open(filepath, 'r') as f:
    content = f.read()

# Replace pass @cast_unchecked<uint8@>("...") with pass @cast_unchecked<int64>("...")
content = re.sub(r'pass @cast_unchecked<uint8@>\(("[^"]+")\);', r'pass @cast_unchecked<int64>(\1);', content)

# Replace pub func:err_str = *uint8(int64:e) {
content = content.replace('pub func:err_str = *uint8(int64:e) {', 'pub func:err_str = int64(int64:e) {')

with open(filepath, 'w') as f:
    f.write(content)
print(f"Fixed {filepath}")
