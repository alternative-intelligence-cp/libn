import re
with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# Replace int64 with any-> in mmap-related wrappers in mmap.npk
# We know mmap.npk defines mem_mmap_raw, mem_munmap_raw, etc.
# These probably also need to take any-> instead of int64.

text = text.replace("pub func:mem_mmap_raw = Result<int64>(int64:addr, int64:length, int64:prot, int64:flags, int64:fd, int64:offset) {", "pub func:mem_mmap_raw = Result<any->>(any->:addr, int64:length, int64:prot, int64:flags, int64:fd, int64:offset) {")
text = text.replace("Result<int64>:r = libn_mmap(addr, length, prot, flags, fd, offset);", "Result<int64>:r = libn_mmap(addr, length, prot, flags, fd, offset);")

# Wait, libn_mmap returns Result<int64> in syscall.npk, but we need to return Result<any->>
# Let's just fix the calls first. We pass `0i64` or `addr` to libn_mmap.
# Actually, I can just replace `libn_mmap(0i64` with `libn_mmap(NULL`

text = text.replace("libn_mmap(0i64,", "libn_mmap(NULL,")
text = text.replace("libn_munmap(0i64,", "libn_munmap(NULL,")
text = text.replace("libn_mprotect(0i64,", "libn_mprotect(NULL,")
text = text.replace("libn_mremap(0i64,", "libn_mremap(NULL,")
text = text.replace("libn_madvise(0i64,", "libn_madvise(NULL,")
text = text.replace("libn_msync(0i64,", "libn_msync(NULL,")

# also fix the variables passed
text = re.sub(r'libn_mmap\((?!NULL)([^,]+),', r'libn_mmap(@cast_unchecked<any->>(\1),', text)
text = re.sub(r'libn_munmap\((?!NULL)([^,]+),', r'libn_munmap(@cast_unchecked<any->>(\1),', text)
text = re.sub(r'libn_mprotect\((?!NULL)([^,]+),', r'libn_mprotect(@cast_unchecked<any->>(\1),', text)
text = re.sub(r'libn_mremap\((?!NULL)([^,]+),', r'libn_mremap(@cast_unchecked<any->>(\1),', text)
text = re.sub(r'libn_madvise\((?!NULL)([^,]+),', r'libn_madvise(@cast_unchecked<any->>(\1),', text)
text = re.sub(r'libn_msync\((?!NULL)([^,]+),', r'libn_msync(@cast_unchecked<any->>(\1),', text)

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

