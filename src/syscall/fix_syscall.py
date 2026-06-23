import re

with open('syscall.npk', 'r') as f:
    code = f.read()

# Replace sys_safe block
code = re.sub(
    r'pub func:sys_safe = Result<int64>\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6\) \{.*?\n\}',
    'pub macro:sys_safe = (nr, a1, a2, a3, a4, a5, a6) { sys(nr, a1, a2, a3, a4, a5, a6) };',
    code, flags=re.DOTALL
)

for i in range(1, 6):
    params = ', '.join([f'int64:a{j}' for j in range(1, i+1)])
    macro_params = ', '.join([f'a{j}' for j in range(1, i+1)])
    args = ', '.join([f'a{j}' for j in range(1, i+1)] + ['0i64'] * (6-i))
    code = re.sub(
        r'pub func:sys' + str(i) + r' = Result<int64>\(int64:nr, ' + params + r'\) \{.*?\n\}',
        f'pub macro:sys{i} = (nr, {macro_params}) {{ sys(nr, {args}) }};',
        code, flags=re.DOTALL
    )

# Replace sys_full block
code = re.sub(
    r'pub func:sys_full = Result<int64>\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6\) \{.*?\n\}',
    'pub macro:sys_full = (nr, a1, a2, a3, a4, a5, a6) { sys!!(nr, a1, a2, a3, a4, a5, a6) };',
    code, flags=re.DOTALL
)

for i in range(1, 6):
    params = ', '.join([f'int64:a{j}' for j in range(1, i+1)])
    macro_params = ', '.join([f'a{j}' for j in range(1, i+1)])
    args = ', '.join([f'a{j}' for j in range(1, i+1)] + ['0i64'] * (6-i))
    code = re.sub(
        r'pub func:sys_full' + str(i) + r' = Result<int64>\(int64:nr, ' + params + r'\) \{.*?\n\}',
        f'pub macro:sys_full{i} = (nr, {macro_params}) {{ sys!!(nr, {args}) }};',
        code, flags=re.DOTALL
    )

# Replace sys_raw block
code = re.sub(
    r'pub func:sys_raw = int64\(int64:nr, int64:a1, int64:a2, int64:a3, int64:a4, int64:a5, int64:a6\) \{.*?\n\}',
    'pub macro:sys_raw = (nr, a1, a2, a3, a4, a5, a6) { sys!!!(nr, a1, a2, a3, a4, a5, a6) };',
    code, flags=re.DOTALL
)

# Now replace the downstream calls
# Examples: 
# Result<int64>:r = sys1(SYS_GETPID, 0i64);
# if (r.is_error) { fail(r.err); }
# pass(r.val);
# -> return sys1!(SYS_GETPID, 0i64);

code = re.sub(
    r'Result<int64>:r = sys([_a-zA-Z0-9]*)\((.*?)\);\n\s*if \(r\.is_error\) \{ fail\(r\.err\); \}\n\s*pass\(r\.val\);',
    r'return sys\1!(\2);',
    code
)
# For the cases where pass(r) was used
code = re.sub(
    r'Result<int64>:r = sys([_a-zA-Z0-9]*)\((.*?)\);\n\s*pass\(r\);',
    r'return sys\1!(\2);',
    code
)
# sys_raw
code = re.sub(
    r'sys_raw\(',
    r'sys_raw!(',
    code
)

with open('syscall.npk', 'w') as f:
    f.write(code)

