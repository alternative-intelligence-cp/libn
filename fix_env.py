import re
with open('src/proc/env.npk', 'r') as f:
    c = f.read()
c = c.replace(
'''    Result<int64>:r = mem_malloc((cap + 1i64) * 8i64);    // +1 for NULL terminator
    if (r.is_error) {''',
'''    Result<int64>:r = mem_malloc((cap + 1i64) * 8i64);    // +1 for NULL terminator
    Result<int64>:r2 = mem_malloc((cap + 1i64) * 8i64);
    if (r.is_error || r2.is_error) {''')
with open('src/proc/env.npk', 'w') as f:
    f.write(c)

