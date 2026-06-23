import re

with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

# 1. Change Result<int64> return types to int64
text = re.sub(r'pub func:([a-zA-Z0-9_]+)\s*=\s*Result<int64>\(', r'pub func:\1 = int64(', text)

# 2. Change pass r; to if (r.is_error) { fail r.error; } pass r.value;
# But only if r is a Result! Wait, we know `r` is the Result from the previous line.
# Let's just find `pass r;` and replace it, but we have to be careful if there are other variables passed.
# Let's just replace `pass r;` because ALL our sys wrapper variables are named `r`!
# Let's verify if `pass r_bot;` or `pass r_top;` exist?
# Actually, the python script generated `Result<int64>:r = sys...; pass r;`
text = re.sub(r'pass r;', r'if (r.is_error) { fail r.error; }\n    pass r.value;', text)

# What about `pass r_bot;`? 
# They were in mmap.npk, not syscall.npk!

# Wait! Did I change libn_open's `pass r;` to `if (r.is_error) { fail r.error; } pass r.value;`?
# Yes, because I used regex to replace `pass r;`.

# 3. Ensure sys!! and sys!!! use SYS_XXX, but sys uses XXX.
# I already replaced sys(SYS_XXX with sys(XXX.
# But wait! I did `re.sub(r'\bsys\(SYS_([A-Z0-9_]+)', r'sys(\1', text)`
# This successfully converted sys(SYS_OPEN to sys(OPEN.
# And sys!!(SYS_MPROTECT was NOT touched because it has `sys!!`, not `sys`.
# So the constants are ALREADY correct!

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)

