import re

path = '/home/randy/Workspace/REPOS/libn/src/io/printf.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """    if (prefix != 0i64) {
        Result<int64>:r = io_write_str(STDERR_FD, prefix);
        if (r.is_error) { return r; }
        int64:r2 = raw io_write_str(STDERR_FD, @cast_unchecked<int64>(@": "));
        if (r2.is_error) { return r2; }
    }"""
new = """    if (prefix != 0i64) {
        int64:r = io_write_str(STDERR_FD, prefix);
        if (r < 0i64) { pass r; }
        int64:r2 = io_write_str(STDERR_FD, @cast_unchecked<int64>(@": "));
        if (r2 < 0i64) { pass r2; }
    }"""

content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)

print("Fixed io_perror")
