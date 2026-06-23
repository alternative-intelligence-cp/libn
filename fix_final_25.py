import os, glob

# Fix test_all.npk
with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('pass 0i32;', 'exit 0i64;')
with open('test_all.npk', 'w') as f:
    f.write(text)

# Fix exec.npk
with open('src/proc/exec.npk', 'r') as f:
    text = f.read()
text = text.replace('=> int64', '')
text = text.replace('@candidate[0] ', '@cast_unchecked<int64>(@candidate[0]) ')
text = text.replace('@argv[0] ', '@cast_unchecked<int64>(@argv[0]) ')
text = text.replace('@"/bin/ls"[0] ', '@cast_unchecked<int64>(@"/bin/ls"[0]) ')
text = text.replace('@"/bin/sh"[0] ', '@cast_unchecked<int64>(@"/bin/sh"[0]) ')
text = text.replace('@"PATH"[0] ', '@cast_unchecked<int64>(@"PATH"[0]) ')
text = text.replace('@"/usr/local/bin:/usr/bin:/bin"[0] ', '@cast_unchecked<int64>(@"/usr/local/bin:/usr/bin:/bin"[0]) ')
text = text.replace('=> int64->', '')
text = text.replace('=> uint8->', '')
text = text.replace('@cast_unchecked<int64->>(argv)', '@cast_unchecked<int64-> >(argv)')
text = text.replace('@cast_unchecked<int64->>(sh_argv_ptr)', '@cast_unchecked<int64-> >(sh_argv_ptr)')
text = text.replace('@cast_unchecked<int64->>(envp)', '@cast_unchecked<int64-> >(envp)')
text = text.replace('@cast_unchecked<uint8->>(path_str)', '@cast_unchecked<uint8-> >(path_str)')
with open('src/proc/exec.npk', 'w') as f:
    f.write(text)

# Fix strerror.npk
with open('src/io/bio/strerror.npk', 'r') as f:
    text = f.read()
import re
text = re.sub(r'msg: (@"[^"]+"\[0\]) => int64', r'msg: @cast_unchecked<int64>(\1)', text)
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(text)
