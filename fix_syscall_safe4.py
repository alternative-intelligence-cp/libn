import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

# I want to change sys(SYS_READ...) to sys(READ...) for all cases where we used sys(SYS_...)
# But only for the ones that don't fail! Which ones failed?
# The ones that failed were:
# SYS_DUP2, SYS_DUP3, SYS_PIPE, SYS_PIPE2, SYS_FCNTL, SYS_IOCTL, SYS_GETPID, SYS_GETPPID, 
# SYS_GETTID, SYS_GETUID, SYS_GETGID, SYS_GETDENTS64, SYS_GETCWD, SYS_READLINKAT, SYS_STATX, 
# SYS_GETRANDOM, SYS_FUTEX, SYS_SET_TID_ADDRESS, SYS_SCHED_GETAFFINITY
# Wait! We need to change SYS_READ to READ, SYS_WRITE to WRITE, etc!

def replace_sys(match):
    prefix = match.group(1)
    constant = match.group(2)
    args = match.group(3)
    if constant.startswith('SYS_'):
        short_name = constant[4:]
        return f"{prefix}sys({short_name}{args}"
    return match.group(0)

# Replace `return sys(SYS_READ, ...)` with `return sys(READ, ...)`
content = re.sub(r'(return\s+)sys\((SYS_[A-Z0-9_]+)(.*?)\)', replace_sys, content)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)

