import re

# Fix write.npk
with open('src/io/write.npk', 'r') as f:
    text = f.read()

text = text.replace('libn_write(fd, buf + total, remaining)', 'libn_write(fd, @cast_unchecked<any->>(buf + total), remaining)')
text = text.replace('libn_write(fd, buf, n)', 'libn_write(fd, @cast_unchecked<any->>(buf), n)')

with open('src/io/write.npk', 'w') as f:
    f.write(text)

# Fix fio.npk
with open('src/io/bio/fio.npk', 'r') as f:
    text = f.read()

text = text.replace('mem_memcpy(dst, f->buf + f->buf_pos, count)', 'mem_memcpy(@cast_unchecked<any->>(dst), @cast_unchecked<any->>(f->buf + f->buf_pos), count)')
text = text.replace('mem_memcpy(f->buf + f->buf_pos, src, to_copy)', 'mem_memcpy(@cast_unchecked<any->>(f->buf + f->buf_pos), @cast_unchecked<any->>(src), to_copy)')
text = text.replace('sys_safe(SYS_READ, f->fd, dst, remaining', 'sys_safe(SYS_READ, f->fd, @cast_unchecked<any->>(dst), remaining')
text = text.replace('sys_safe(SYS_WRITE, f->fd, src, remaining', 'sys_safe(SYS_WRITE, f->fd, @cast_unchecked<any->>(src), remaining')

with open('src/io/bio/fio.npk', 'w') as f:
    f.write(text)

