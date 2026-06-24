import re

with open('src/io/bio/fio.npk', 'r') as f:
    text = f.read()

# Undo sys_safe mistakes
text = text.replace('sys_safe(SYS_READ, f->fd, @cast_unchecked<any->>(dst), remaining', 'sys_safe(SYS_READ, f->fd, dst, remaining')
text = text.replace('sys_safe(SYS_WRITE, f->fd, @cast_unchecked<any->>(src), remaining', 'sys_safe(SYS_WRITE, f->fd, src, remaining')

# Fix mem_memcpy correctly
text = re.sub(r'mem_memcpy\(\s*dst\s*,\s*f->buf\s*\+\s*f->buf_pos\s*,\s*count\s*\)', 
              r'mem_memcpy(@cast_unchecked<any->>(dst), @cast_unchecked<any->>(f->buf + f->buf_pos), count)', text)
text = re.sub(r'mem_memcpy\(\s*f->buf\s*\+\s*f->buf_pos\s*,\s*src\s*,\s*to_copy\s*\)', 
              r'mem_memcpy(@cast_unchecked<any->>(f->buf + f->buf_pos), @cast_unchecked<any->>(src), to_copy)', text)

with open('src/io/bio/fio.npk', 'w') as f:
    f.write(text)

