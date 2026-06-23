import re
path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk'
with open(path, 'r') as f:
    content = f.read()

# Change `int64:parse_ok = bio_parse_mode(...)` to `Result<int64>:parse_ok = bio_parse_mode(...)`
# And `if (parse_ok != 0i64)` to `if (parse_ok.is_error)`
content = content.replace('int64:parse_ok = bio_parse_mode', 'Result<int64>:parse_ok = bio_parse_mode')
content = content.replace('if (parse_ok != 0i64) {', 'if (parse_ok.is_error) {')

with open(path, 'w') as f:
    f.write(content)
print("Fixed parse_ok")
