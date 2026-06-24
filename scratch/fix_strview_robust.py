import re

with open('src/str/strview.npk', 'r') as f:
    text = f.read()

# I will just write explicit replacements for exactly what's failing.
# Looking at the original file (no casts yet)
replacements = [
    # str_strlen
    (r'str_strlen\(s\)', r'str_strlen(@cast_unchecked<any->>(s))'),
    (r'str_strlen\(ptr\)', r'str_strlen(@cast_unchecked<any->>(ptr))'),
    
    # mem_memcpy
    (r'mem_memcpy\(@cast_unchecked<int64>\(@tmp\), s->ptr, s->len\)', r'mem_memcpy(@cast_unchecked<any->>(@cast_unchecked<int64>(@tmp)), @cast_unchecked<any->>(s->ptr), s->len)'),
    (r'mem_memcpy\(buf, s->ptr, s->len\)', r'mem_memcpy(@cast_unchecked<any->>(buf), @cast_unchecked<any->>(s->ptr), s->len)'),
    (r'mem_memcpy\(buf, s->ptr, n\)', r'mem_memcpy(@cast_unchecked<any->>(buf), @cast_unchecked<any->>(s->ptr), n)'),
    (r'mem_memcpy\(r\.value, s->ptr, s->len\)', r'mem_memcpy(@cast_unchecked<any->>(r.value), @cast_unchecked<any->>(s->ptr), s->len)'),
    
    # str_parse
    (r'str_parse_i64\(@cast_unchecked<int64>\(@tmp\)\)', r'str_parse_i64(@cast_unchecked<any->>(@cast_unchecked<int64>(@tmp)))'),
    (r'str_parse_i64\(buf\)', r'str_parse_i64(@cast_unchecked<any->>(buf))'),
    (r'str_parse_u64\(@cast_unchecked<int64>\(@tmp\)\)', r'str_parse_u64(@cast_unchecked<any->>(@cast_unchecked<int64>(@tmp)))'),
    (r'str_parse_u64\(buf\)', r'str_parse_u64(@cast_unchecked<any->>(buf))'),
    
    # libn_write_all
    (r'libn_write_all\(fd, s->ptr, s->len\)', r'libn_write_all(fd, @cast_unchecked<any->>(s->ptr), s->len)'),
    
    # strcmp / strcasecmp / etc.
    (r'str_strcmp\(s->ptr, s2\)', r'str_strcmp(@cast_unchecked<any->>(s->ptr), @cast_unchecked<any->>(s2))'),
    (r'str_strncmp\(s->ptr, s2, n\)', r'str_strncmp(@cast_unchecked<any->>(s->ptr), @cast_unchecked<any->>(s2), n)'),
    (r'str_strcasecmp\(s->ptr, s2\)', r'str_strcasecmp(@cast_unchecked<any->>(s->ptr), @cast_unchecked<any->>(s2))'),
    (r'str_strncasecmp\(s->ptr, s2, n\)', r'str_strncasecmp(@cast_unchecked<any->>(s->ptr), @cast_unchecked<any->>(s2), n)'),
    (r'str_casecmp_prefix\(s->ptr, prefix\)', r'str_casecmp_prefix(@cast_unchecked<any->>(s->ptr), @cast_unchecked<any->>(prefix))'),
]

for orig, new in replacements:
    text = re.sub(orig, new, text)

# add missing imports
imports = """use "../syscall/errno.npk".*;
use "../syscall/syscall.npk".*;
use "../mem/slab.npk".*;
use "../str/strchr.npk".*;
use "../str/strcmp.npk".*;
use "../mem/mmap.npk".*;"""

text = re.sub(r'use "../syscall/errno.npk".*;\nuse "../mem/mmap.npk".*;', imports, text)

with open('src/str/strview.npk', 'w') as f:
    f.write(text)

