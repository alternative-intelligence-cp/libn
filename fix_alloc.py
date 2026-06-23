import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk'
with open(path, 'r') as f:
    content = f.read()

# Fix bio_alloc_file
alloc_file_orig = """pub func:bio_alloc_file = int64() {
    int64:p = raw slab_alloc_zero(80i64);    // 80 bytes = sizeof(FILE), goes in 128-uint8 class
    if (p == 0i64) {
        pass 0i64;
    }"""
alloc_file_new = """pub func:bio_alloc_file = int64() {
    Result<int64>:r_p = slab_alloc_zero(80i64);    // 80 bytes = sizeof(FILE), goes in 128-uint8 class
    if (r_p.is_error) { pass 0i64; }
    int64:p = r_p.value;
    if (p == 0i64) {
        pass 0i64;
    }"""
content = content.replace(alloc_file_orig, alloc_file_new)

# Fix bio_alloc_buf
alloc_buf_orig = """pub func:bio_alloc_buf = int64(int64:size) {
    if (size <= 0i64) {
        pass 0i64;
    }
    if (size <= 4096i64) {
        pass slab_alloc_zero(size);
    }
    pass raw mem_malloc(size);
}"""
alloc_buf_new = """pub func:bio_alloc_buf = int64(int64:size) {
    if (size <= 0i64) {
        pass 0i64;
    }
    if (size <= 4096i64) {
        Result<int64>:r1 = slab_alloc_zero(size);
        if (r1.is_error) { pass 0i64; }
        pass r1.value;
    }
    Result<int64>:r2 = mem_malloc(size);
    if (r2.is_error) { pass 0i64; }
    pass r2.value;
}"""
content = content.replace(alloc_buf_orig, alloc_buf_new)

with open(path, 'w') as f:
    f.write(content)

# Revert fstate.npk change since bio_alloc_buf now returns int64 again
fstate_path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fstate.npk'
with open(fstate_path, 'r') as f:
    fstate = f.read()

fstate_new = fstate.replace("""        Result<int64>:r_newbuf = bio_alloc_buf(cap);
        if (r_newbuf.is_error) {""", """        int64:newbuf = bio_alloc_buf(cap);
        if (newbuf == 0i64) {""").replace("""        }
        int64:newbuf = r_newbuf.value;
        f.buf     = newbuf;""", """        }
        f.buf     = newbuf;""")

with open(fstate_path, 'w') as f:
    f.write(fstate_new)

print("Fixed allocs")
