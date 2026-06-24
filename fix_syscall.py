import re

with open('src/syscall/syscall.npk', 'r') as f:
    code = f.read()

cases = [
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

pick_cases = []
for case in cases:
    pick_cases.append(f"        ({case}) {{ ret = sys!!!(nr, a1, a2, a3, a4, a5, a6); }}")
pick_cases.append("        (*) { fail @cast_unchecked<tbb32>(EPERM); }")

replacement = "    int64:ret = 0i64;\n    pick (nr) {\n" + "\n".join(pick_cases) + "\n    }\n    pass err_from_syscall(ret);"

pattern = r"    int64:ret = sys!!!\(nr, a1, a2, a3, a4, a5, a6\);\n    pass err_from_syscall\(ret\);"
new_code = code.replace(pattern, replacement, 1)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(new_code)
