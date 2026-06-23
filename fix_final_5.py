import re

# exec.npk
with open('src/proc/exec.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'extern int64:environ;' in lines[i]:
        lines[i] = 'extern { int64:environ; };\n'
    elif 'int64:null_idx = (argc == 0i64) ? 2i64 : 1i64 + argc;' in lines[i]:
        lines[i] = '                int64:null_idx = 1i64 + argc; if (argc == 0i64) { null_idx = 2i64; }\n'
    elif 'int64:eff_dir_len = (dir_len > 0i64) ? dir_len : 1i64;' in lines[i]:
        lines[i] = '        int64:eff_dir_len = 1i64; if (dir_len > 0i64) { eff_dir_len = dir_len; }\n'
with open('src/proc/exec.npk', 'w') as f:
    f.writelines(lines)

# strtok.npk
with open('src/str/strtok.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    if 'struct StrField {' in lines[i]:
        lines[i] = 'struct:StrField = {\n'
    elif 'f.@cast_unchecked<uint8->>(ptr);' in lines[i]:
        lines[i] = '    uint8->:fp = @cast_unchecked<uint8->>(f.ptr);\n'
with open('src/str/strtok.npk', 'w') as f:
    f.writelines(lines)
