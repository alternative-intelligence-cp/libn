import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

whitelist = """
    pick (nr) {
        (SYS_READ) { return sys(SYS_READ, a1, a2, a3, a4, a5, a6); },
        (SYS_WRITE) { return sys(SYS_WRITE, a1, a2, a3, a4, a5, a6); },
        (SYS_OPEN) { return sys(SYS_OPEN, a1, a2, a3, a4, a5, a6); },
        (SYS_CLOSE) { return sys(SYS_CLOSE, a1, a2, a3, a4, a5, a6); },
        (SYS_STAT) { return sys(SYS_STAT, a1, a2, a3, a4, a5, a6); },
        (SYS_FSTAT) { return sys(SYS_FSTAT, a1, a2, a3, a4, a5, a6); },
        (SYS_LSTAT) { return sys(SYS_LSTAT, a1, a2, a3, a4, a5, a6); },
        (SYS_LSEEK) { return sys(SYS_LSEEK, a1, a2, a3, a4, a5, a6); },
        (SYS_MMAP) { return sys(SYS_MMAP, a1, a2, a3, a4, a5, a6); },
        (SYS_MUNMAP) { return sys(SYS_MUNMAP, a1, a2, a3, a4, a5, a6); },
        (SYS_MPROTECT) { return sys(SYS_MPROTECT, a1, a2, a3, a4, a5, a6); },
        (SYS_MADVISE) { return sys(SYS_MADVISE, a1, a2, a3, a4, a5, a6); },
        (SYS_BRK) { return sys(SYS_BRK, a1, a2, a3, a4, a5, a6); },
        (SYS_MREMAP) { return sys(SYS_MREMAP, a1, a2, a3, a4, a5, a6); },
        (SYS_DUP) { return sys(SYS_DUP, a1, a2, a3, a4, a5, a6); },
        (SYS_DUP2) { return sys(SYS_DUP2, a1, a2, a3, a4, a5, a6); },
        (SYS_DUP3) { return sys(SYS_DUP3, a1, a2, a3, a4, a5, a6); },
        (SYS_PIPE) { return sys(SYS_PIPE, a1, a2, a3, a4, a5, a6); },
        (SYS_PIPE2) { return sys(SYS_PIPE2, a1, a2, a3, a4, a5, a6); },
        (SYS_FCNTL) { return sys(SYS_FCNTL, a1, a2, a3, a4, a5, a6); },
        (SYS_IOCTL) { return sys(SYS_IOCTL, a1, a2, a3, a4, a5, a6); },
        (SYS_GETPID) { return sys(SYS_GETPID, a1, a2, a3, a4, a5, a6); },
        (SYS_GETPPID) { return sys(SYS_GETPPID, a1, a2, a3, a4, a5, a6); },
        (SYS_GETTID) { return sys(SYS_GETTID, a1, a2, a3, a4, a5, a6); },
        (SYS_GETUID) { return sys(SYS_GETUID, a1, a2, a3, a4, a5, a6); },
        (SYS_GETGID) { return sys(SYS_GETGID, a1, a2, a3, a4, a5, a6); },
        (SYS_GETDENTS64) { return sys(SYS_GETDENTS64, a1, a2, a3, a4, a5, a6); },
        (SYS_GETCWD) { return sys(SYS_GETCWD, a1, a2, a3, a4, a5, a6); },
        (SYS_READLINKAT) { return sys(SYS_READLINKAT, a1, a2, a3, a4, a5, a6); },
        (SYS_STATX) { return sys(SYS_STATX, a1, a2, a3, a4, a5, a6); },
        (SYS_GETRANDOM) { return sys(SYS_GETRANDOM, a1, a2, a3, a4, a5, a6); },
        (SYS_FUTEX) { return sys(SYS_FUTEX, a1, a2, a3, a4, a5, a6); },
        (SYS_SET_TID_ADDRESS) { return sys(SYS_SET_TID_ADDRESS, a1, a2, a3, a4, a5, a6); },
        (SYS_SCHED_GETAFFINITY) { return sys(SYS_SCHED_GETAFFINITY, a1, a2, a3, a4, a5, a6); },
        (_) {
            return err_from_syscall(-1i64); // EPERM essentially
        }
    }
"""

old_block = """pub func:sys_safe = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {
    int64:ret = sys!!!(nr, a1, a2, a3, a4, a5, a6);
    return err_from_syscall(ret);
}"""

new_block = f"""pub func:sys_safe = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {{{whitelist}}}"""

content = content.replace(old_block, new_block)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)
print("Updated sys_safe")
