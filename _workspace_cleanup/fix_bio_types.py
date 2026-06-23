import re

with open('src/io/bio/file.npk', 'r') as f:
    text = f.read()

# file.npk line 117
text = text.replace('int64:p = slab_alloc(bio_file_slab);', 'int64:p = raw slab_alloc(bio_file_slab);')
# file.npk line 132
text = text.replace('slab_free(fp);', 'slab_free(bio_file_slab, fp);')
# file.npk line 153
text = text.replace('slab_free(bio_buf_slab_8k, ptr);', 'slab_free(bio_buf_slab_8k, ptr);') # wait, what was it originally?
text = text.replace('slab_free(ptr);', 'slab_free(bio_buf_slab_8k, ptr);')
# Wait, let's use regex for slab_free(ptr)
text = re.sub(r'slab_free\(([a-zA-Z0-9_]+)\);', r'slab_free(bio_file_slab, \1);', text)
text = text.replace('slab_free(bio_file_slab, bio_buf_slab_8k, ptr);', 'slab_free(bio_buf_slab_8k, ptr);')
text = text.replace('slab_free(bio_file_slab, bio_file_slab, fp);', 'slab_free(bio_file_slab, fp);')

# line 146 mem_malloc
text = text.replace('mem_malloc', 'slab_alloc') # Wait, BUFSIZ is 8192, maybe sys_mmap? Let's just raw sys_mmap.
text = text.replace('int64:ptr = mem_malloc(size);', 'int64:ptr = raw slab_alloc(bio_buf_slab_8k);') # wait, I don't know the size
# I will use sed to check lines 140-160 later if this fails.

# line 165 pass 0i64 vs Result
text = text.replace('pub func:bio_flush_write_buf = Result<int64>(int64:fp) {', 'pub func:bio_flush_write_buf = int64(int64:fp) {')
text = text.replace('func:bio_flush_write_buf = Result<int64>(int64:fp) {', 'pub func:bio_flush_write_buf = int64(int64:fp) {')
text = text.replace('int64:e = @cast_unchecked<int64>(r.error);\n            if (e == EINTR) { continue; }\n            f.flags = f.flags | FILE_FLAG_ERROR;\n            fail r.error;\n        }\n        if (r.value == 0i64)', 'int64:e = @cast_unchecked<int64>(r.error);\n            if (e == EINTR) { continue; }\n            f.flags = f.flags | FILE_FLAG_ERROR;\n            pass -1i64;\n        }\n        if (r.value == 0i64)')
text = text.replace('f.flags = f.flags | FILE_FLAG_ERROR;\n            fail r.error;', 'f.flags = f.flags | FILE_FLAG_ERROR;\n            pass -1i64;')

# line 172 sys_safe
text = text.replace('Result<int64>:r = sys_safe(', 'Result<int64>:r = sys_safe(') # wait sys_safe is undefined? Maybe sys_write?
text = text.replace('sys_safe(SYS_WRITE', 'sys_write(SYS_WRITE')
text = text.replace('sys_safe(SYS_READ', 'sys_read(SYS_READ')
# Actually, libn provides sys_write? I should check sys.npk. Let's just use raw sys_write? No, `Result<int64>` is returned by sys_safe?
# I'll check sys.npk next.

with open('src/io/bio/file.npk', 'w') as f:
    f.write(text)

with open('src/io/bio/fopen.npk', 'r') as f:
    text = f.read()

# line 134 Result<Result<int64>>
text = text.replace('Result<Result<int64>>:init_r', 'Result<int64>:init_r')
text = text.replace('Result<int64>:init_r = libn_open(path, open_flags, FOPEN_CREAT_MODE);', 'Result<int64>:init_r = libn_open(path, open_flags, FOPEN_CREAT_MODE);')
# Actually, I changed libn_open to return Result<int64>. If libn_open is returning Result, `Result<int64>:r = libn_open` is fine.

with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(text)

