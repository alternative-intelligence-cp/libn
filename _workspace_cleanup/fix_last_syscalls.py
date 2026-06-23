import re
with open('src/syscall/syscall.npk', 'r') as f:
    text = f.read()

# Replace sys(MADVISE, ...) with sys!!(SYS_MADVISE, ...)
text = re.sub(r'sys\(MADVISE,', r'sys!!(SYS_MADVISE,', text)
text = re.sub(r'sys\(MSYNC,', r'sys!!(SYS_MSYNC,', text)
text = re.sub(r'sys\(CLOCK_GETRES,', r'sys!!(SYS_CLOCK_GETRES,', text)
text = re.sub(r'sys\(SCHED_YIELD,', r'sys!!(SYS_SCHED_YIELD,', text)
text = re.sub(r'sys\(FUTEX,', r'sys!!(SYS_FUTEX,', text)

# There might be others like EXIT or EXIT_GROUP
text = re.sub(r'sys\(EXIT,', r'sys!!!(SYS_EXIT,', text)
text = re.sub(r'sys\(EXIT_GROUP,', r'sys!!!(SYS_EXIT_GROUP,', text)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(text)

