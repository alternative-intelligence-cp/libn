import os

with open('src/proc/exec.npk', 'r') as f:
    text = f.read()
text = text.replace('pass execl(path, &argv[0] as int64);', 'pass(execl(path, @cast_unchecked<int64>(@argv[0])));')
text = text.replace('pass execle(path, &argv[0] as int64, environ);', 'pass(execle(path, @cast_unchecked<int64>(@argv[0]), environ));')
text = text.replace('pass execlp(name, &argv[0] as int64);', 'pass(execlp(name, @cast_unchecked<int64>(@argv[0])));')
text = text.replace('&argv[0] as int64', '@cast_unchecked<int64>(@argv[0])')
text = text.replace('pass execlp', 'return execlp')
text = text.replace('pass exec', 'return exec')
with open('src/proc/exec.npk', 'w') as f:
    f.write(text)

with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()
text = text.replace('pub func:libn_write_all = int64(int64:fd, int64:buf, int64:nbytes)', 'pub func:libn_write_all = Result<int64>(int64:fd, int64:buf, int64:nbytes)')
text = text.replace('pub func:libn_read_retry = int64(int64:fd, int64:buf, int64:nbytes)', 'pub func:libn_read_retry = Result<int64>(int64:fd, int64:buf, int64:nbytes)')
with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)

