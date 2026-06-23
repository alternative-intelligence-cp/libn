import re
with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

text = text.replace('if (prot & PROT_EXEC) != 0i64 {', 'if ((prot & PROT_EXEC) != 0i64) {')
text = text.replace('fail ERR_BADARG as tbb8;', 'fail ERR_BADARG;') # Actually, ERR_BADARG is already tbb8?
# Let's check posix_constants.npk... ERR_BADARG might be int64. But let's just use @cast_unchecked<tbb8>(ERR_BADARG)
text = text.replace('fail ERR_BADARG as tbb8;', 'fail @cast_unchecked<tbb8>(ERR_BADARG);')
text = text.replace('while remaining > 0i64 {', 'while (remaining > 0i64) {')
text = text.replace('if r.is_error {', 'if (r.is_error) {')
text = text.replace('if r.err as int64 == EINTR {', 'if (@cast_unchecked<int64>(r.error) == EINTR) {')
text = text.replace('fail r.err;', 'fail r.error;')
text = text.replace('if n == 0i64 {', 'if (n == 0i64) {')
text = text.replace('if w == 0i64 {', 'if (w == 0i64) {')
text = text.replace('if written > 0i64 {', 'if (written > 0i64) {')
text = text.replace('if remaining > 0i64 {', 'if (remaining > 0i64) {')

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)
