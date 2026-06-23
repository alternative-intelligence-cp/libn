path = '/home/randy/Workspace/REPOS/libn/src/mem/slab.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """pub func:slab_alloc_zero = int64(int64:n) {
    int64:r = slab_alloc(n);
    if (r.is_error) {
        fail r.error;
    }
    int64:ptr = r.value;"""

new = """pub func:slab_alloc_zero = int64(int64:n) {
    int64:r = slab_alloc(n);
    if (r == 0i64) {
        pass 0i64;
    }
    int64:ptr = r;"""

content = content.replace(orig, new)

with open(path, 'w') as f:
    f.write(content)

print("Fixed slab_alloc_zero")
