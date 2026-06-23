import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

def repl_sys_read(m):
    return '''    while (true) {
        int64:res = libn_read(f.fd, f.buf, f.buf_cap);
        if (res < 0i64) {
            int64:e = 0i64 - res;
            if (e == EINTR) { continue; }
            f.flags = f.flags | FILE_FLAG_ERROR;
            pass -1i64;
        }
        if (res == 0i64) {
            f.flags = f.flags | FILE_FLAG_EOF;
            pass 0i64;
        }
        f.buf_len = res;
        pass res;
    }'''

text = re.sub(r'    while \(true\)\{?.*?pass r\.value;\n    \}', repl_sys_read, text, flags=re.DOTALL)
text = text.replace('fail ERR_BADARG;', 'pass -1i64;')

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

