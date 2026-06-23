import os, glob

# Fix strbuf.npk
with open('src/str/strbuf.npk', 'r') as f:
    text = f.read()
text = text.replace('int64:tmp_ptr = @tmp[0] => int64;', 'int64:tmp_ptr = @cast_unchecked<int64>(@tmp[0]);')
with open('src/str/strbuf.npk', 'w') as f:
    f.write(text)

# Fix strfmt.npk (add missing str_snprintf5 and str_snprintf7)
with open('src/str/strfmt.npk', 'r') as f:
    text = f.read()

func5 = """
pub func:str_snprintf5 = int64(int64:buf, int64:buf_size, int64:fmt,
                               int64:a0, int64:a1, int64:a2, int64:a3, int64:a4) {
    stack int64[5]:args;
    args[0] = a0; args[1] = a1; args[2] = a2; args[3] = a3; args[4] = a4;
    pass(str_vsnprintf(buf, buf_size, fmt, @cast_unchecked<int64>(@args[0]), 5i64));
}
"""

func7 = """
pub func:str_snprintf7 = int64(int64:buf, int64:buf_size, int64:fmt,
                               int64:a0, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {
    stack int64[7]:args;
    args[0] = a0; args[1] = a1; args[2] = a2; args[3] = a3; args[4] = a4; args[5] = a5; args[6] = a6;
    pass(str_vsnprintf(buf, buf_size, fmt, @cast_unchecked<int64>(@args[0]), 7i64));
}
"""

if 'str_snprintf5' not in text:
    text = text.replace('pub func:str_snprintf6 = int64(', func5 + '\npub func:str_snprintf6 = int64(')
if 'str_snprintf7' not in text:
    text = text.replace('pub func:str_snprintf8 = int64(', func7 + '\npub func:str_snprintf8 = int64(')

with open('src/str/strfmt.npk', 'w') as f:
    f.write(text)

# Fix strview.npk missing import
with open('src/str/strview.npk', 'r') as f:
    text = f.read()
if 'write.npk' not in text:
    text = text.replace('use "src/syscall/syscall.npk".*;\n', 'use "src/syscall/syscall.npk".*;\nuse "src/io/write.npk".*;\n')
with open('src/str/strview.npk', 'w') as f:
    f.write(text)

# Fix file.npk missing import
with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()
if 'syscall_numbers.npk' not in text:
    text = text.replace('use "src/syscall/syscall.npk".*;\n', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;\n')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

# Fix test_all.npk pass
with open('test_all.npk', 'r') as f:
    text = f.read()
text = text.replace('\n    pass;\n', '\n    exit 0i64;\n')
with open('test_all.npk', 'w') as f:
    f.write(text)

