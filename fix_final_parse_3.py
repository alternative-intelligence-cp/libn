# Fix signal.npk
with open("src/proc/signal.npk", "r") as f:
    content = f.read()

content = content.replace("sys!!", "sys")

# Fix & and pointers in sigprocmask
old_sigprocmask = """pub func:sigprocmask = int64(int64:how, int64:set, int64:old_ptr) {
    // SYS_RT_SIGPROCMASK: (how, set*, old*, sigsetsize)
    // set and old are pointers to sigset_t (int64 here)
    stack int64:set_val;
    set_val = set;
    stack int64:old_val;
    int64:old_p = &old_val;
    if (!(old_ptr != 0i64) { old_p = 0i64; }

    int64:r = sys(SYS_RT_SIGPROCMASK,
                             how,
                             &set_val,
                             old_p,
                             8i64,
                             0i64, 0i64);
    if (r.is_error) {
        libn_errno_set(@cast_unchecked<int64>(r.error));
        pass -1i64;
    }

    if (old_ptr != 0i64) {
        *(@cast_unchecked<int64->>(old_ptr)) = old_val;
    }

    pass 0i64;
};"""

new_sigprocmask = """pub func:sigprocmask = int64(int64:how, int64:set, int64:old_ptr) {
    stack int64[1]:set_val;
    set_val[0] = set;
    stack int64[1]:old_val;
    int64:old_p = @cast_unchecked<int64>(old_val);
    if (!(old_ptr != 0i64)) { old_p = 0i64; }

    int64:r = sys(SYS_RT_SIGPROCMASK,
                             how,
                             @cast_unchecked<int64>(set_val),
                             old_p,
                             8i64,
                             0i64, 0i64);
    if (r < 0i64) {
        libn_errno_set(-r);
        pass -1i64;
    }

    if (old_ptr != 0i64) {
        (@cast_unchecked<int64->>(old_ptr))[0] = old_val[0];
    }

    pass 0i64;
};"""

content = content.replace(old_sigprocmask, new_sigprocmask)

# Fix raise
old_raise = """pub func:raise = int64(int64:signo) {
    // Use tkill(gettid(), signo) for correct per-thread delivery.
    // Since we're single-threaded, getpid()==gettid(). Use SYS_TKILL.
    Result<int64>:res_es_pid_r = sys(GETPID, 0i64, 0i64, 0i64, 0i64, 0i64, 0i64);
    if (res_es_pid_r.is_error) { fail @cast_unchecked<tbb8>(res_es_pid_r.error); }
    es_pid_r = res_es_pid_r.value;
    if (res_pid_r.is_error) { fail @cast_unchecked<tbb8>(res_pid_r.error); }
    int64:pid_r = res_pid_r.value;
    int64:tid = 1i64;
    if (!(pid_r.is_error) { tid = pid_r.value; }
    int64:r = sys(SYS_TKILL, tid, signo, 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        libn_errno_set(@cast_unchecked<int64>(r.error));
        pass -1i64;
    }
    pass 0i64;
};"""

new_raise = """pub func:raise = int64(int64:signo) {
    int64:pid_r = sys(SYS_GETPID, 0i64, 0i64, 0i64, 0i64, 0i64, 0i64);
    int64:tid = pid_r;
    int64:r = sys(SYS_TKILL, tid, signo, 0i64, 0i64, 0i64, 0i64);
    if (r < 0i64) {
        libn_errno_set(-r);
        pass -1i64;
    }
    pass 0i64;
};"""

content = content.replace(old_raise, new_raise)

# Fix sigaction
old_sigact = """    int64:r = sys(SYS_RT_SIGACTION,
                             signo,
                             @cast_unchecked<int64>(new_act),
                             old_ptr,
                             8i64,
                             0i64, 0i64);
    if (r.is_error) {
        libn_errno_set(@cast_unchecked<int64>(r.error));
        pass -1i64;
    }"""
new_sigact = """    int64:r = sys(SYS_RT_SIGACTION,
                             signo,
                             @cast_unchecked<int64>(new_act),
                             old_ptr,
                             8i64,
                             0i64, 0i64);
    if (r < 0i64) {
        libn_errno_set(-r);
        pass -1i64;
    }"""
content = content.replace(old_sigact, new_sigact)

# Fix kill
old_kill = """pub func:kill = int64(int64:pid, int64:signo) {
    int64:r = sys(SYS_KILL, pid, signo, 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        libn_errno_set(@cast_unchecked<int64>(r.error));
        pass -1i64;
    }
    pass 0i64;
};"""

new_kill = """pub func:kill = int64(int64:pid, int64:signo) {
    int64:r = sys(SYS_KILL, pid, signo, 0i64, 0i64, 0i64, 0i64);
    if (r < 0i64) {
        libn_errno_set(-r);
        pass -1i64;
    }
    pass 0i64;
};"""

content = content.replace(old_kill, new_kill)

with open("src/proc/signal.npk", "w") as f:
    f.write(content)

# Replace strerror.npk to use giant if/else
strerror_content = """// strerror.npk — errno to human-readable string table
use "src/syscall/errno.npk".*;
use "src/str/strlen.npk".*;
use "src/str/strconv.npk".*;
use "src/mem/memcpy.npk".*;
use "src/io/bio/file.npk".*;
use "src/io/bio/fio.npk".*;
use "src/io/bio/fchar.npk".*;
use "src/io/bio/fstr.npk".*;
use "src/io/bio/stdfiles.npk".*;

byte[64]:g_strerror_unknown_buf;

pub func:strerror = int64(int64:errnum) {
    if (errnum == 0i64) { pass "Success" as int64; }
    if (errnum == 1i64) { pass "Operation not permitted" as int64; }
    if (errnum == 2i64) { pass "No such file or directory" as int64; }
    if (errnum == 3i64) { pass "No such process" as int64; }
    if (errnum == 4i64) { pass "Interrupted system call" as int64; }
    if (errnum == 5i64) { pass "Input/output error" as int64; }
    if (errnum == 6i64) { pass "No such device or address" as int64; }
    if (errnum == 7i64) { pass "Argument list too long" as int64; }
    if (errnum == 8i64) { pass "Exec format error" as int64; }
    if (errnum == 9i64) { pass "Bad file descriptor" as int64; }
    if (errnum == 10i64) { pass "No child processes" as int64; }
    if (errnum == 11i64) { pass "Resource temporarily unavailable" as int64; }
    if (errnum == 12i64) { pass "Cannot allocate memory" as int64; }
    if (errnum == 13i64) { pass "Permission denied" as int64; }
    if (errnum == 14i64) { pass "Bad address" as int64; }
    if (errnum == 15i64) { pass "Block device required" as int64; }
    if (errnum == 16i64) { pass "Device or resource busy" as int64; }
    if (errnum == 17i64) { pass "File exists" as int64; }
    if (errnum == 18i64) { pass "Invalid cross-device link" as int64; }
    if (errnum == 19i64) { pass "No such device" as int64; }
    if (errnum == 20i64) { pass "Not a directory" as int64; }
    if (errnum == 21i64) { pass "Is a directory" as int64; }
    if (errnum == 22i64) { pass "Invalid argument" as int64; }
    if (errnum == 23i64) { pass "Too many open files in system" as int64; }
    if (errnum == 24i64) { pass "Too many open files" as int64; }
    if (errnum == 25i64) { pass "Inappropriate ioctl for device" as int64; }
    if (errnum == 26i64) { pass "Text file busy" as int64; }
    if (errnum == 27i64) { pass "File too large" as int64; }
    if (errnum == 28i64) { pass "No space left on device" as int64; }
    if (errnum == 29i64) { pass "Illegal seek" as int64; }
    if (errnum == 30i64) { pass "Read-only file system" as int64; }
    if (errnum == 31i64) { pass "Too many links" as int64; }
    if (errnum == 32i64) { pass "Broken pipe" as int64; }
    if (errnum == 33i64) { pass "Numerical argument out of domain" as int64; }
    if (errnum == 34i64) { pass "Numerical result out of range" as int64; }
    if (errnum == 35i64) { pass "Resource deadlock avoided" as int64; }
    if (errnum == 36i64) { pass "File name too long" as int64; }
    if (errnum == 37i64) { pass "No locks available" as int64; }
    if (errnum == 38i64) { pass "Function not implemented" as int64; }
    if (errnum == 39i64) { pass "Directory not empty" as int64; }
    if (errnum == 40i64) { pass "Too many levels of symbolic links" as int64; }
    if (errnum == 42i64) { pass "No message of desired type" as int64; }
    if (errnum == 43i64) { pass "Identifier removed" as int64; }
    if (errnum == 61i64) { pass "No data available" as int64; }
    if (errnum == 62i64) { pass "Timer expired" as int64; }
    if (errnum == 63i64) { pass "Out of streams resources" as int64; }
    if (errnum == 67i64) { pass "Link has been severed" as int64; }
    if (errnum == 71i64) { pass "Protocol error" as int64; }
    if (errnum == 72i64) { pass "Multihop attempted" as int64; }
    if (errnum == 74i64) { pass "Bad message" as int64; }
    if (errnum == 75i64) { pass "Value too large for defined data type" as int64; }
    if (errnum == 84i64) { pass "Invalid or incomplete multibyte or wide character" as int64; }
    if (errnum == 88i64) { pass "Socket operation on non-socket" as int64; }
    if (errnum == 89i64) { pass "Destination address required" as int64; }
    if (errnum == 90i64) { pass "Message too long" as int64; }
    if (errnum == 91i64) { pass "Protocol wrong type for socket" as int64; }
    if (errnum == 92i64) { pass "Protocol not available" as int64; }
    if (errnum == 93i64) { pass "Protocol not supported" as int64; }
    if (errnum == 95i64) { pass "Operation not supported" as int64; }
    if (errnum == 97i64) { pass "Address family not supported by protocol" as int64; }
    if (errnum == 98i64) { pass "Address already in use" as int64; }
    if (errnum == 99i64) { pass "Cannot assign requested address" as int64; }
    if (errnum == 100i64) { pass "Network is down" as int64; }
    if (errnum == 101i64) { pass "Network is unreachable" as int64; }
    if (errnum == 102i64) { pass "Network dropped connection on reset" as int64; }
    if (errnum == 103i64) { pass "Software caused connection abort" as int64; }
    if (errnum == 104i64) { pass "Connection reset by peer" as int64; }
    if (errnum == 105i64) { pass "No buffer space available" as int64; }
    if (errnum == 106i64) { pass "Transport endpoint is already connected" as int64; }
    if (errnum == 107i64) { pass "Transport endpoint is not connected" as int64; }
    if (errnum == 110i64) { pass "Connection timed out" as int64; }
    if (errnum == 111i64) { pass "Connection refused" as int64; }
    if (errnum == 113i64) { pass "No route to host" as int64; }
    if (errnum == 114i64) { pass "Operation already in progress" as int64; }
    if (errnum == 115i64) { pass "Operation now in progress" as int64; }
    if (errnum == 116i64) { pass "Stale file handle" as int64; }
    if (errnum == 125i64) { pass "Operation canceled" as int64; }
    if (errnum == 130i64) { pass "Owner died" as int64; }
    if (errnum == 131i64) { pass "State not recoverable" as int64; }

    uint8->:dst = @cast_unchecked<uint8->>(g_strerror_unknown_buf);
    fixed byte:prefix[15] = "Unknown error ";
    int64:prefix_len = str_strlen(@cast_unchecked<int64>(prefix));
    drop mem_memcpy(@cast_unchecked<int64>(dst), @cast_unchecked<int64>(prefix), prefix_len);
    stack byte[24]:num;
    int64:num_len = str_int64_to_dec(errnum, @cast_unchecked<int64>(num), 24i64);
    drop mem_memcpy(@cast_unchecked<int64>(dst[prefix_len]), @cast_unchecked<int64>(num), num_len + 1i64);
    pass @cast_unchecked<int64>(g_strerror_unknown_buf);
};

pub func:strerror_r = int64(int64:errnum, int64:buf, int64:buflen) {
    if (buf == 0i64 || buflen <= 0i64) {
        pass EINVAL;
    }

    int64:msg = strerror(errnum);
    int64:msg_len = str_strlen(msg);

    if (msg_len + 1i64 > buflen) {
        drop mem_memcpy(buf, msg, buflen - 1i64);
        (@cast_unchecked<uint8->>(buf))[buflen - 1i64] = 0u8;
        pass ERANGE;
    }

    drop mem_memcpy(buf, msg, msg_len + 1i64);
    pass 0i64;
};

pub func:perror = NIL(int64:prefix) {
    bio_ensure_std_init();

    if (prefix != 0i64 && (@cast_unchecked<uint8->>(prefix))[0] != 0u8) {
        drop fputs(prefix, stderr_fp);
        drop fputc(58i64, stderr_fp);   // ':'
        drop fputc(32i64, stderr_fp);   // ' '
    }

    int64:msg = strerror(@cast_unchecked<int64>(libn_errno));
    drop fputs(msg, stderr_fp);
    drop fputc(10i64, stderr_fp);   // '\n'
    drop fflush(stderr_fp);
};
"""

with open("src/io/bio/strerror.npk", "w") as f:
    f.write(strerror_content)

