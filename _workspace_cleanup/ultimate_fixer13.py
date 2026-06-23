import os

# 1. memutil.npk
with open('src/mem/memutil.npk', 'r') as f:
    code = f.read()
code = code.replace('int64:x = (v - ones) & (!v) & mask;', 'int64:x = (v - ones) & (~v) & mask;')
with open('src/mem/memutil.npk', 'w') as f:
    f.write(code)

# 2. fchar.npk
with open('src/io/bio/fchar.npk', 'r') as f:
    code = f.read()

# Lines 86-91
old_fchar_1 = """            if (r.value == 0i64) {
                f.flags = f.flags | FILE_FLAG_EOF;
                pass FILE_EOF;
            }
            f.file_pos = f.file_pos + 1i64;
            pass @cast_unchecked<int64>(one[0]);"""
new_fchar_1 = """            int64:v = 0i64; if (!r.is_error) { v = r.value; }
            if (v == 0i64) {
                f.flags = f.flags | FILE_FLAG_EOF;
                pass FILE_EOF;
            }
            f.file_pos = f.file_pos + 1i64;
            pass @cast_unchecked<int64>(one[0]);"""
code = code.replace(old_fchar_1, new_fchar_1)

# Line 100
old_fchar_2 = """        if (r.is_error || r.value == 0i64) {"""
new_fchar_2 = """        int64:v = 0i64; if (!r.is_error) { v = r.value; }
        if (r.is_error || v == 0i64) {"""
code = code.replace(old_fchar_2, new_fchar_2)

with open('src/io/bio/fchar.npk', 'w') as f:
    f.write(code)

# 3. fio.npk
with open('src/io/bio/fio.npk', 'r') as f:
    code = f.read()

old_fio_1 = """                if (r.value == 0i64) {
                    f.flags = f.flags | FILE_FLAG_EOF;
                    break;
                }
                f.file_pos = f.file_pos + r.value;
                dst        = dst + r.value;
                bytes_read = bytes_read + r.value;"""
new_fio_1 = """                int64:v = 0i64; if (!r.is_error) { v = r.value; }
                if (v == 0i64) {
                    f.flags = f.flags | FILE_FLAG_EOF;
                    break;
                }
                f.file_pos = f.file_pos + v;
                dst        = dst + v;
                bytes_read = bytes_read + v;"""
code = code.replace(old_fio_1, new_fio_1)

old_fio_2 = """                if (r.value == 0i64) {
                    break;  // EOF
                }"""
new_fio_2 = """                int64:v = 0i64; if (!r.is_error) { v = r.value; }
                if (v == 0i64) {
                    break;  // EOF
                }"""
code = code.replace(old_fio_2, new_fio_2)

old_fio_3 = """            f.file_pos    = f.file_pos + r.value;
            src            = src + r.value;
            bytes_written  = bytes_written + r.value;"""
new_fio_3 = """            int64:v = 0i64; if (!r.is_error) { v = r.value; }
            f.file_pos    = f.file_pos + v;
            src            = src + v;
            bytes_written  = bytes_written + v;"""
code = code.replace(old_fio_3, new_fio_3)

old_fio_4 = """            f.file_pos    = f.file_pos + wr.value;
            src            = src + wr.value;
            bytes_written  = bytes_written + wr.value;"""
new_fio_4 = """            int64:v = 0i64; if (!wr.is_error) { v = wr.value; }
            f.file_pos    = f.file_pos + v;
            src            = src + v;
            bytes_written  = bytes_written + v;"""
code = code.replace(old_fio_4, new_fio_4)

with open('src/io/bio/fio.npk', 'w') as f:
    f.write(code)

# 4. file.npk
with open('src/io/bio/file.npk', 'r') as f:
    code = f.read()

old_file_1 = """        if (r.value == 0i64) {
            f.flags = f.flags | FILE_FLAG_ERROR;
            fail @cast_unchecked<tbb8>(ERR_AGAIN);  // 0-byte write is an error for buffered I/O
        }
        ptr = ptr + r.value;
        f.file_pos = f.file_pos + r.value;
        remaining = remaining - r.value;"""
new_file_1 = """        int64:v = 0i64; if (!r.is_error) { v = r.value; }
        if (v == 0i64) {
            f.flags = f.flags | FILE_FLAG_ERROR;
            fail @cast_unchecked<tbb8>(ERR_AGAIN);  // 0-byte write is an error for buffered I/O
        }
        ptr = ptr + v;
        f.file_pos = f.file_pos + v;
        remaining = remaining - v;"""
code = code.replace(old_file_1, new_file_1)

with open('src/io/bio/file.npk', 'w') as f:
    f.write(code)

print("Applied ultimate_fixer13.py")
