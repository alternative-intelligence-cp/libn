import re

path = '/home/randy/Workspace/REPOS/libn/src/time/timeofday.npk'
with open(path, 'r') as f:
    content = f.read()

orig1 = """    if (tv == 0i64) {"""
new1 = """    if (@cast_unchecked<int64>(tv) == 0i64) {"""
content = content.replace(orig1, new1)

orig2 = """    Result<int64>:r = sys(GETTIMEOFDAY, @cast_unchecked<int64>(tv), tz,
0i64, 0i64, 0i64, 0i64);
    if (r.is_error == true) {
        pass(libn_errno_set(@cast_unchecked<int64>(r.error)));
    }"""
new2 = """    Result<int64>:r = sys_safe(SYS_GETTIMEOFDAY, @cast_unchecked<int64>(tv), tz, 0i64, 0i64, 0i64, 0i64);
    if (r.is_error) {
        pass errno_set(@cast_unchecked<int64>(r.error));
    }"""
content = content.replace(orig2.replace('\n', ''), new2.replace('\n', '')) # quick hack, use regex
content = re.sub(r'Result<int64>:r = sys\(GETTIMEOFDAY.*?\).*?;', r'Result<int64>:r = sys_safe(SYS_GETTIMEOFDAY, @cast_unchecked<int64>(tv), tz, 0i64, 0i64, 0i64, 0i64);', content, flags=re.DOTALL)

content = re.sub(r'Result<int64>:r = sys\(SETTIMEOFDAY.*?\).*?;', r'Result<int64>:r = sys_safe(SYS_SETTIMEOFDAY, @cast_unchecked<int64>(tv), tz, 0i64, 0i64, 0i64, 0i64);', content, flags=re.DOTALL)

content = content.replace("libn_errno_set", "errno_set")
content = content.replace("r.is_error == true", "r.is_error")

with open(path, 'w') as f:
    f.write(content)
print("Fixed timeofday.npk")

path = '/home/randy/Workspace/REPOS/libn/src/time/clock.npk'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('if (tp == 0i64) {', 'if (@cast_unchecked<int64>(tp) == 0i64) {')
content = content.replace('if (res == 0i64) {', 'if (@cast_unchecked<int64>(res) == 0i64) {')
with open(path, 'w') as f:
    f.write(content)
print("Fixed clock.npk pointers")
