import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

bad_syscalls = [
    "SYS_DUP2", "SYS_DUP3", "SYS_PIPE", "SYS_PIPE2", "SYS_FCNTL", "SYS_IOCTL",
    "SYS_GETPID", "SYS_GETPPID", "SYS_GETTID", "SYS_GETUID", "SYS_GETGID",
    "SYS_GETDENTS64", "SYS_GETCWD", "SYS_READLINKAT", "SYS_STATX", "SYS_GETRANDOM",
    "SYS_FUTEX", "SYS_SET_TID_ADDRESS", "SYS_SCHED_GETAFFINITY"
]

for bad in bad_syscalls:
    # (SYS_DUP2) { return sys(SYS_DUP2, a1, a2, a3, a4, a5, a6); },
    old_line = f"({bad}) {{ return sys({bad}, a1, a2, a3, a4, a5, a6); }},"
    new_line = f"({bad}) {{ return err_from_syscall(sys!!!({bad}, a1, a2, a3, a4, a5, a6)); }},"
    content = content.replace(old_line, new_line)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)
