import re

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fio.npk', 'r') as f:
    content = f.read()

# Fix block 1
block1_old = """                Result<int64>:res_es_r = sys(READ, f->fd, dst, remaining, 0i64, 0i64, 0i64);
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_es_r.error); }
    dst = res_es_r.value;
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_r.error); }
    int64:r = res_es_r.value;
                if (r.is_error) {
                    int64:e = @cast_unchecked<int64>(r.error);
                    if (e == EINTR) { continue; }
                    f->flags = f->flags | FILE_FLAG_ERROR;
                    break;
                }
                if (r.value == 0i64) {
                    f->flags = f->flags | FILE_FLAG_EOF;
                    break;
                }
                f.file_pos = f.file_pos + f.value;
                dst        = dst + f.value;
                bytes_read = bytes_read + f.value;"""

block1_new = """                Result<int64>:r = sys3(SYS_READ, f->fd, dst, remaining);
                if (r.is_error) {
                    if (@cast_unchecked<int64>(r.error) == EINTR) { continue; }
                    f->flags = f->flags | FILE_FLAG_ERROR;
                    break;
                }
                if (r.value == 0i64) {
                    f->flags = f->flags | FILE_FLAG_EOF;
                    break;
                }
                f->file_pos = f->file_pos + r.value;
                dst         = dst + r.value;
                bytes_read  = bytes_read + r.value;"""
content = content.replace(block1_old, block1_new)

# Fix block 2
block2_old = """            Result<int64>:res_es_r = sys(WRITE, f->fd, src, remaining, 0i64, 0i64, 0i64);
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_es_r.error); }
    src = res_es_r.value;
    if (res_es_r.is_error) { fail @cast_unchecked<tbb8>(res_r.error); }
    int64:r = res_es_r.value;
            if (r.is_error) {
                int64:e = @cast_unchecked<int64>(r.error);
                if (e == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                break;
            }
            f.file_pos    = f.file_pos + f.value;
            src            = src + f.value;
            bytes_written  = bytes_written + r.value;"""

block2_new = """            Result<int64>:r = sys3(SYS_WRITE, f->fd, src, remaining);
            if (r.is_error) {
                if (@cast_unchecked<int64>(r.error) == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                break;
            }
            f->file_pos    = f->file_pos + r.value;
            src            = src + r.value;
            bytes_written  = bytes_written + r.value;"""
content = content.replace(block2_old, block2_new)

# Fix block 3
block3_old = """            Result<int64>:res_es_wr = sys(WRITE, f->fd, src, remaining, 0i64, 0i64, 0i64);
    if (res_es_wr.is_error) { fail @cast_unchecked<tbb8>(res_es_wr.error); }
    es_wr = res_es_wr.value;
    if (res_es_wr.is_error) { fail @cast_unchecked<tbb8>(res_wr.error); }
    int64:wr = res_es_wr.value;
            if (src.is_error) {
                int64:e = @cast_unchecked<int64>(wr.error);
                if (e == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                break;
            }
            f.file_pos    = f.file_pos + src.value;
            src            = src + src.value;
            bytes_written  = bytes_written + src.value;"""

block3_new = """            Result<int64>:wr = sys3(SYS_WRITE, f->fd, src, remaining);
            if (wr.is_error) {
                if (@cast_unchecked<int64>(wr.error) == EINTR) { continue; }
                f->flags = f->flags | FILE_FLAG_ERROR;
                break;
            }
            f->file_pos    = f->file_pos + wr.value;
            src            = src + wr.value;
            bytes_written  = bytes_written + wr.value;"""
content = content.replace(block3_old, block3_new)

content = content.replace('if (f.is_error) {', 'if (r.is_error) {')
content = content.replace('if (f.value == 0i64) {', 'if (r.value == 0i64) {')
content = content.replace('f.unget = FILE_UNGET_EMPTY;', 'f->unget = FILE_UNGET_EMPTY;')
content = content.replace('f.file_pos = f.file_pos + 1i64;', 'f->file_pos = f->file_pos + 1i64;')

content = content.replace('f.buf_len - f.buf_pos', 'f->buf_len - f->buf_pos')
content = content.replace('f.buf_pos  = f.buf_pos + to_copy;', 'f->buf_pos  = f->buf_pos + to_copy;')
content = content.replace('f.file_pos = f.file_pos + to_copy;', 'f->file_pos = f->file_pos + to_copy;')
content = content.replace('f.buf_mode == _IONBF', 'f->buf_mode == _IONBF')
content = content.replace('f.buf_cap', 'f->buf_cap')
content = content.replace('f.buf_pos == 0i64', 'f->buf_pos == 0i64')
content = content.replace('f.buf_pos     = f.buf_pos + to_copy;', 'f->buf_pos     = f->buf_pos + to_copy;')
content = content.replace('f.buf_len     = f.buf_pos;', 'f->buf_len     = f->buf_pos;')

with open('/home/randy/Workspace/REPOS/libn/src/io/bio/fio.npk', 'w') as f:
    f.write(content)

