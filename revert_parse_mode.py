import os

file_path = '/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace('pub func:bio_parse_mode = Result<int64>(', 'pub func:bio_parse_mode = int64(')

with open(file_path, 'w') as f:
    f.write(content)

fopen_path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk'
with open(fopen_path, 'r') as f:
    content = f.read()

content = content.replace('Result<int64>:parse_ok = bio_parse_mode', 'int64:parse_ok = bio_parse_mode')
content = content.replace('if (parse_ok.is_error) {', 'if (parse_ok != 0i64) {')

with open(fopen_path, 'w') as f:
    f.write(content)

print("Reverted parse_mode")
