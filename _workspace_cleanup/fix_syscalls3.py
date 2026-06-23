import re
with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

# 1. Change libn_* from int64( to Result<int64>(
def repl_sig(m):
    name = m.group(1)
    if name in ['libn_exit_group', 'libn_exit_thread']:
        return m.group(0) # Keep NIL
    return f"pub func:{name} = Result<int64>("

content = re.sub(r'pub func:(libn_[a-zA-Z0-9_]*) = int64\(', repl_sig, content)

# 2. Fix sysX and sys_fullX to correctly pass Results
def repl_sysX(m):
    call = m.group(1)
    args = m.group(2)
    return f"Result<int64>:ret = {call}({args});\n    if (ret.is_error) {{ fail ret.error; }}\n    pass ret.value;"

content = re.sub(r'pass (?:raw )?(sys_safe|sys_full)\(([^)]+)\);', repl_sysX, content)

# 3. Fix `Result<int64>:r = sys(...); pass r;` to unwrap correctly
def repl_pass_r(m):
    return "if (r.is_error) { fail r.error; }\n    pass r.value;"

content = re.sub(r'pass r;', repl_pass_r, content)
content = re.sub(r'pass ret;', 'if (ret.is_error) { fail ret.error; }\n    pass ret.value;', content)
content = re.sub(r'pass rr;', 'if (rr.is_error) { fail rr.error; }\n    pass rr.value;', content)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
