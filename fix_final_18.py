import os, glob

# Fix strbuf pub
with open('src/str/strbuf.npk', 'r') as f:
    text = f.read()
text = text.replace('\nstruct:StrBuf', '\npub struct:StrBuf')
with open('src/str/strbuf.npk', 'w') as f:
    f.write(text)

# Fix .err to .error globally
for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as f:
        text = f.read()
    if '.err)' in text or '.err;' in text:
        text = text.replace('.err)', '.error)')
        text = text.replace('.err;', '.error;')
        with open(file, 'w') as f:
            f.write(text)

# Fix @tmp[0] => int64 in strview.npk
with open('src/str/strview.npk', 'r') as f:
    text = f.read()
text = text.replace('@tmp[0] => int64', '@cast_unchecked<int64>(@tmp[0])')
with open('src/str/strview.npk', 'w') as f:
    f.write(text)

# Fix libn_write_all pub in io/write.npk
with open('src/io/write.npk', 'r') as f:
    text = f.read()
text = text.replace('\nfunc:libn_write_all', '\npub func:libn_write_all')
with open('src/io/write.npk', 'w') as f:
    f.write(text)

# Add syscall_numbers.npk to fio.npk and fseek.npk
with open('src/io/bio/fseek.npk', 'r') as f:
    text = f.read()
if 'syscall_numbers.npk' not in text:
    text = text.replace('use "src/syscall/syscall.npk".*;\n', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;\n')
    with open('src/io/bio/fseek.npk', 'w') as f:
        f.write(text)

with open('src/io/bio/fchar.npk', 'r') as f:
    text = f.read()
if 'syscall_numbers.npk' not in text:
    text = text.replace('use "src/syscall/syscall.npk".*;\n', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;\n')
    with open('src/io/bio/fchar.npk', 'w') as f:
        f.write(text)

