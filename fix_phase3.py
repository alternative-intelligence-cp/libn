import re

# Phase 3.1: Hardware Acceleration via Memory Intrinsics
with open("src/mem/memcpy.npk", "r") as f:
    memcpy = f.read()

memcpy = re.sub(
    r'pub func:mem_memcpy = int64\(int64:dst, int64:src, int64:num_bytes\) \{.*?^};',
    r'''pub func:mem_memcpy = int64(int64:dst, int64:src, int64:num_bytes) requires dst != 0i64 && src != 0i64 {
    drop(mcpy(dst, src, num_bytes));
    pass dst;
};''',
    memcpy,
    flags=re.MULTILINE | re.DOTALL
)

memcpy = re.sub(
    r'pub func:mem_memmove = int64\(int64:dst, int64:src, int64:num_bytes\) \{.*?^};',
    r'''pub func:mem_memmove = int64(int64:dst, int64:src, int64:num_bytes) requires dst != 0i64 && src != 0i64 {
    drop(mmov(dst, src, num_bytes));
    pass dst;
};''',
    memcpy,
    flags=re.MULTILINE | re.DOTALL
)

with open("src/mem/memcpy.npk", "w") as f:
    f.write(memcpy)

with open("src/mem/memset.npk", "r") as f:
    memset = f.read()

memset = re.sub(
    r'pub func:mem_memset = int64\(int64:ptr, int64:c, int64:n\) \{.*?^};',
    r'''pub func:mem_memset = int64(int64:ptr, int64:c, int64:n) {
    if (ptr != 0i64) {
        drop(memset(ptr, c, n));
    }
    pass ptr;
};''',
    memset,
    flags=re.MULTILINE | re.DOTALL
)

with open("src/mem/memset.npk", "w") as f:
    f.write(memset)

# Phase 3.2: CFI Violation in atexit
with open("src/proc/exit.npk", "r") as f:
    exit_npk = f.read()

exit_npk = exit_npk.replace(
    '''            (NIL)():handler = fn => (NIL)();
              // 2. Invoke it, using _? (drop) to discard the implicitly returned Result
            _? handler();''',
    '''            drop asm!!!<int64>("x86_64", "call *%0", "r", fn);'''
)
exit_npk = exit_npk.replace(
    '''            (NIL)():handler = fn => (NIL)();
            _? handler();''',
    '''            drop asm!!!<int64>("x86_64", "call *%0", "r", fn);'''
)

with open("src/proc/exit.npk", "w") as f:
    f.write(exit_npk)

# Phase 3.3: Prevent Stack Bloat in memmem
with open("src/mem/memutil.npk", "r") as f:
    memutil = f.read()

memutil = memutil.replace("stack int64[256]:bad_char;", "stack uint16[256]:bad_char;")
memutil = memutil.replace("bad_char[0] = nlen;", "bad_char[0] = @cast_unchecked<uint16>(nlen);")
memutil = memutil.replace("bad_char[i] = nlen;", "bad_char[i] = @cast_unchecked<uint16>(nlen);")
memutil = memutil.replace("bad_char[@cast_unchecked<int64>(n[i])] = nlen - 1i64 - i;", "bad_char[@cast_unchecked<int64>(n[i])] = @cast_unchecked<uint16>(nlen - 1i64 - i);")
memutil = memutil.replace("offset = offset + bad_char[@cast_unchecked<int64>(h[offset + nlen - 1i64])];", "offset = offset + @cast_unchecked<int64>(bad_char[@cast_unchecked<int64>(h[offset + nlen - 1i64])]);")

with open("src/mem/memutil.npk", "w") as f:
    f.write(memutil)

