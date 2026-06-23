import re

def fix_file(path, ptrs):
    with open(path, 'r') as f:
        content = f.read()
    
    for ptr in ptrs:
        # Match ptr == 0i64 or ptr != 0i64
        # We also need to be careful if it's already casted
        content = re.sub(rf'\b{ptr}\s*(==|!=)\s*0i64\b', rf'@cast_unchecked<int64>({ptr}) \1 0i64', content)
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('/home/randy/Workspace/REPOS/libn/src/str/strconv.npk', ['endptr'])
fix_file('/home/randy/Workspace/REPOS/libn/src/str/strtok.npk', ['saveptr', 'stringp'])

print("Fixed pointers in strconv and strtok")
