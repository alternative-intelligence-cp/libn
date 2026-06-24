with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

whitelist = [
    "SYS_READ", "SYS_WRITE", "SYS_OPEN", "SYS_CLOSE",
    "SYS_STAT", "SYS_FSTAT", "SYS_LSTAT", "SYS_LSEEK", "SYS_MMAP", "SYS_MUNMAP",
    "SYS_MPROTECT", "SYS_MADVISE", "SYS_BRK", "SYS_MREMAP",
    "SYS_DUP", "SYS_DUP2", "SYS_DUP3", "SYS_PIPE", "SYS_PIPE2",
    "SYS_FCNTL", "SYS_IOCTL",
    "SYS_GETPID", "SYS_GETPPID", "SYS_GETTID", "SYS_GETUID", "SYS_GETGID",
    "SYS_GETEUID", "SYS_GETEGID",
    "SYS_CLOCK_GETTIME", "SYS_CLOCK_GETRES", "SYS_GETTIMEOFDAY",
    "SYS_NANOSLEEP", "SYS_SCHED_YIELD",
    "SYS_OPENAT", "SYS_NEWFSTATAT", "SYS_UNLINKAT", "SYS_MKDIRAT",
    "SYS_GETDENTS64", "SYS_GETCWD", "SYS_READLINKAT",
    "SYS_STATX", "SYS_GETRANDOM",
    "SYS_FUTEX", "SYS_SET_TID_ADDRESS", "SYS_SCHED_GETAFFINITY"
]

pick_cases = ", ".join(whitelist)

target = """pub func:sys_safe = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {
    int64:ret = sys!!!(nr, a1, a2, a3, a4, a5, a6);
    return err_from_syscall(ret);
};"""

replacement = f"""pub func:sys_safe = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {{
    int64:ret = -1i64; // EPERM or ENOSYS ideally
    if (nr == SYS_READ || nr == SYS_WRITE || nr == SYS_OPEN || nr == SYS_CLOSE ||
        nr == SYS_STAT || nr == SYS_FSTAT || nr == SYS_LSTAT || nr == SYS_LSEEK ||
        nr == SYS_MMAP || nr == SYS_MUNMAP || nr == SYS_MPROTECT || nr == SYS_MADVISE ||
        nr == SYS_BRK || nr == SYS_MREMAP || nr == SYS_DUP || nr == SYS_DUP2 ||
        nr == SYS_DUP3 || nr == SYS_PIPE || nr == SYS_PIPE2 || nr == SYS_FCNTL ||
        nr == SYS_IOCTL || nr == SYS_GETPID || nr == SYS_GETPPID || nr == SYS_GETTID ||
        nr == SYS_GETUID || nr == SYS_GETGID || nr == SYS_GETEUID || nr == SYS_GETEGID ||
        nr == SYS_CLOCK_GETTIME || nr == SYS_CLOCK_GETRES || nr == SYS_GETTIMEOFDAY ||
        nr == SYS_NANOSLEEP || nr == SYS_SCHED_YIELD || nr == SYS_OPENAT ||
        nr == SYS_NEWFSTATAT || nr == SYS_UNLINKAT || nr == SYS_MKDIRAT ||
        nr == SYS_GETDENTS64 || nr == SYS_GETCWD || nr == SYS_READLINKAT ||
        nr == SYS_STATX || nr == SYS_GETRANDOM || nr == SYS_FUTEX ||
        nr == SYS_SET_TID_ADDRESS || nr == SYS_SCHED_GETAFFINITY) {{
        ret = sys!!!(nr, a1, a2, a3, a4, a5, a6);
    }} else {{
        fail @cast_unchecked<tbb32>(EPERM); // Reject unauthorized syscalls
    }}
    return err_from_syscall(ret);
}};"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/syscall/syscall.npk', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Target not found.")
