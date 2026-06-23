with open('src/io/bio/strerror.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'code) ? 101i64' in lines[i]:
        lines[i] = lines[i].replace('code) ? 101i64', 'code: 101i64')
    if 'msg : @' in lines[i]:
        lines[i] = lines[i].replace('msg : @', 'msg: @')
    if 'uint8[64]) ? g_strerror_unknown_buf;' in lines[i]:
        lines[i] = lines[i].replace('uint8[64]) ?', 'uint8[64]:')
with open('src/io/bio/strerror.npk', 'w') as f:
    f.writelines(lines)

with open('src/proc/exec.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'extern "C" { int64:environ; };' in lines[i]:
        lines[i] = 'extern "C" { int64:environ; }\n'
with open('src/proc/exec.npk', 'w') as f:
    f.writelines(lines)
