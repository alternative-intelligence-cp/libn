import os, glob, re

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()

    text = re.sub(r'@cast_unchecked<([a-zA-Z0-9_]+)->>(\()', r'@cast_unchecked<\1-> >\2', text)
    # Also fix printf.npk line 398 and memcpy.npk line 60
    text = text.replace('int64:msg = _!err_str@cast_unchecked<int64>((e));', 'int64:msg = _!err_str(e);')
    text = text.replace('int64->:di_word = (dst + i));', 'int64->:di_word = @cast_unchecked<int64-> >(dst + i);')
    text = text.replace('dst @cast_unchecked<int64->>((aligned', 'dst is aligned')
    text = text.replace('@cast_unchecked<int64->>(old_ptr)', '@cast_unchecked<int64-> >(old_ptr)')

    with open(file, 'w') as f:
        f.write(text)

