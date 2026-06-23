import re

path1 = '/home/randy/Workspace/REPOS/libn/src/io/bio/fio.npk'
with open(path1, 'r') as f:
    content = f.read()
content = content.replace('Result<int64>:r = drop bio_refill_read_buf(fp);', 'Result<int64>:r = bio_refill_read_buf(fp);')
with open(path1, 'w') as f:
    f.write(content)

path2 = '/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk'
with open(path2, 'r') as f:
    content = f.read()
content = content.replace('Result<int64>:r = drop bio_refill_read_buf(fp);', 'Result<int64>:r = bio_refill_read_buf(fp);')
with open(path2, 'w') as f:
    f.write(content)

print("Fixed drop")
