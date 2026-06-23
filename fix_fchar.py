import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk', 'r') as file:
    content = file.read()

# Fix fgetc block
block1_old = """            Result<int64>:res_es_r = sys(READ, f->fd, @cast_unchecked<int64>(one), 1i64, 0i64, 0i64, 0i64);
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_es_r.error); }
    es_r = res_es_r.value;
    if (res_r.is_error) { fail @cast_unchecked<tbb8>(res_r.error); }
    int64:r = res_r.value;
            if (r.is_error) {
                int64:e = @cast_unchecked<int64>(r.error);
                if (e == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                pass FILE_EOF;
            }
            if (f.value == 0i64) {
                f->flags = f->flags | FILE_FLAG_EOF;
                pass FILE_EOF;
            }"""

block1_new = """            Result<int64>:r = sys3(SYS_READ, f->fd, @cast_unchecked<int64>(one), 1i64);
            if (r.is_error) {
                if (@cast_unchecked<int64>(r.error) == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                pass FILE_EOF;
            }
            if (r.value == 0i64) {
                f->flags = f->flags | FILE_FLAG_EOF;
                pass FILE_EOF;
            }"""
content = content.replace(block1_old, block1_new)

# Fix fputc block
block2_old = """            Result<int64>:res_es_r = sys(WRITE, f->fd, @cast_unchecked<int64>(one), 1i64, 0i64, 0i64, 0i64);
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_es_r.error); }
    es_r = res_es_r.value;
    if (res_r.is_error) { fail @cast_unchecked<tbb8>(res_r.error); }
    int64:r = res_r.value;
            if (r.is_error) {
                int64:e = @cast_unchecked<int64>(r.error);
                if (e == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                pass FILE_EOF;
            }"""

block2_new = """            Result<int64>:r = sys3(SYS_WRITE, f->fd, @cast_unchecked<int64>(one), 1i64);
            if (r.is_error) {
                if (@cast_unchecked<int64>(r.error) == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                pass FILE_EOF;
            }"""
content = content.replace(block2_old, block2_new)

content = content.replace('f.unget    = FILE_UNGET_EMPTY;', 'f->unget = FILE_UNGET_EMPTY;')
content = content.replace('f.file_pos = f.file_pos + 1i64;', 'f->file_pos = f->file_pos + 1i64;')
content = content.replace('f.value == 0i64', 'r.value == 0i64')

# Fix b replacement
content = content.replace('(@cast_unchecked<uint8->>(f->buf))[f.buf_pos] = f;', '(@cast_unchecked<uint8->>(f->buf))[f->buf_pos] = b;')
content = content.replace('f->buf_pos = f.buf_pos + 1i64;', 'f->buf_pos = f->buf_pos + 1i64;')
content = content.replace('f->buf_len = f.buf_pos;', 'f->buf_len = f->buf_pos;')
content = content.replace('if (f->buf_mode == _IOLBF && f == 10u8) {', 'if (f->buf_mode == _IOLBF && b == 10u8) {')
content = content.replace('if (f.is_error) {', 'if (r.is_error) {')
content = content.replace('f.buf_pos', 'f->buf_pos')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fchar.npk', 'w') as file:
    file.write(content)

