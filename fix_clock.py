import re

path = '/home/randy/Workspace/REPOS/libn/src/time/clock.npk'
with open(path, 'r') as f:
    content = f.read()

orig = """    int64:r = libn_clock_gettime(clockid, @cast_unchecked<int64>(tp));
    if (r.is_error == true) {
        pass(libn_errno_set(@cast_unchecked<int64>(r.error)));
    }"""
new = """    Result<int64>:r = sys_safe(SYS_CLOCK_GETTIME, clockid, @cast_unchecked<int64>(tp), 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        pass errno_set(@cast_unchecked<int64>(r.error));
    }"""
content = content.replace(orig, new)

orig2 = """    Result<int64>:r = sys(CLOCK_GETRES, clockid, @cast_unchecked<int64>(res), 0i64, 0i64, 0i64, 0i64);
    if (r.is_error == true) {
        pass(libn_errno_set(@cast_unchecked<int64>(r.error)));
    }"""
new2 = """    Result<int64>:r = sys_safe(SYS_CLOCK_GETRES, clockid, @cast_unchecked<int64>(res), 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        pass errno_set(@cast_unchecked<int64>(r.error));
    }"""
content = content.replace(orig2, new2)

orig3 = """    Result<int64>:r = sys(CLOCK_SETTIME, clockid, @cast_unchecked<int64>(tp), 0i64, 0i64, 0i64, 0i64);
    if (r.is_error == true) {

        pass(libn_errno_set(@cast_unchecked<int64>(r.error)));
    }"""
new3 = """    Result<int64>:r = sys_safe(SYS_CLOCK_SETTIME, clockid, @cast_unchecked<int64>(tp), 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        pass errno_set(@cast_unchecked<int64>(r.error));
    }"""
content = content.replace(orig3, new3)

# Also fix libn_errno_set to errno_set
content = content.replace("libn_errno_set", "errno_set")

with open(path, 'w') as f:
    f.write(content)
print("Fixed clock.npk")
