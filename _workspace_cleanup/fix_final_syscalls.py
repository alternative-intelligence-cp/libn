import re
with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

# Fix void return types
text = re.sub(r'pub func:([a-zA-Z0-9_]+)\s*=\s*void\(', r'pub func:\1 = NIL(', text)

# Fix GETCWD
text = re.sub(r'sys\(\s*GETCWD\s*(?:,\s*0i64\s*)*\)', r'sys(GETCWD)', text)

# Map of constants to replace sys(NAME, -> sys!!(SYS_NAME,
unsafe_syscalls = [
    'STATX', 'FCHDIR', 'SET_TID_ADDRESS', 'MADVISE', 'MSYNC',
    'CLOCK_GETRES', 'SCHED_YIELD', 'FUTEX'
]

for sc in unsafe_syscalls:
    text = re.sub(rf'sys\(\s*{sc}\s*,', f'sys!!(SYS_{sc},', text)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)

