import re

with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

# Let's just fix sys1 through sys6 manually since it's cleaner.

content = re.sub(
    r'pub func:sys1 = int64\(int64:nr, int64:a1\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys1 = int64(int64:nr, int64:a1) {\n    Result<int64>:r = sys_safe(nr, a1, 0i64, 0i64, 0i64, 0i64, 0i64);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

content = re.sub(
    r'pub func:sys2 = int64\(int64:nr, int64:a1, int64:a2\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys2 = int64(int64:nr, int64:a1, int64:a2) {\n    Result<int64>:r = sys_safe(nr, a1, a2, 0i64, 0i64, 0i64, 0i64);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

content = re.sub(
    r'pub func:sys3 = int64\(int64:nr, int64:a1, int64:a2, int64:a3\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys3 = int64(int64:nr, int64:a1, int64:a2, int64:a3) {\n    Result<int64>:r = sys_safe(nr, a1, a2, a3, 0i64, 0i64, 0i64);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

content = re.sub(
    r'pub func:sys4 = int64\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys4 = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4) {\n    Result<int64>:r = sys_safe(nr, a1, a2, a3, a4, 0i64, 0i64);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

content = re.sub(
    r'pub func:sys5 = int64\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys5 = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5) {\n    Result<int64>:r = sys_safe(nr, a1, a2, a3, a4, a5, 0i64);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

content = re.sub(
    r'pub func:sys6 = int64\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6\) \{\n    Result<int64>:r = sys_safe\(sys_safe\);\n    if \(r\.is_error\) \{ fail r\.error; \}\n    pass r\.value;\n\};',
    r'pub func:sys6 = int64(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6) {\n    Result<int64>:r = sys_safe(nr, a1, a2, a3, a4, a5, a6);\n    if (r.is_error) { fail r.error; }\n    pass r.value;\n};',
    content
)

# And now fix sys_full1 through sys_full6

def full_replacer(m):
    num = m.group(1)
    args = m.group(2)
    inner_args = m.group(3)
    return f"pub func:sys_full{num} = int64({args}) {{\n    Result<int64>:r = sys_full({inner_args});\n    if (r.is_error) {{ fail r.error; }}\n    pass r.value;\n}};"

content = re.sub(
    r'pub func:sys_full(\d+) = int64\((.*?)\) \{\n    pass raw sys_full\((.*?)\);\n\};',
    full_replacer,
    content,
    flags=re.DOTALL
)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
