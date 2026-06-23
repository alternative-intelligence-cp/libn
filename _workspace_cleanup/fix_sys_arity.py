import re

with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

def replacer(m):
    num = m.group(1)
    args = m.group(2)
    inner_args = m.group(3)
    return f"pub func:sys{num} = int64({args}) {{\n    Result<int64>:r = sys_safe({inner_args});\n    if (r.is_error) {{ fail r.error; }}\n    pass r.value;\n}};"

# Match pub func:sys1 = int64(int64:nr, int64:a1) {\n    pass raw sys_safe(nr, a1, 0i64, 0i64, 0i64, 0i64, 0i64);\n};
content = re.sub(
    r'pub func:sys(\d|full\d) = int64\((.*?)\) \{\n    pass raw (sys_safe|sys_full)\((.*?)\);\n\};',
    replacer,
    content,
    flags=re.DOTALL
)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
