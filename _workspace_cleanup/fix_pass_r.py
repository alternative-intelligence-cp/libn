import re

with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

# Replace all forms of pass r; pass rr; pass ret;
content = re.sub(r'pass r;', r'if (r.is_error) { fail r.error; }\n    pass r.value;', content)
content = re.sub(r'pass rr;', r'if (rr.is_error) { fail rr.error; }\n    pass rr.value;', content)
content = re.sub(r'pass ret;', r'if (ret.is_error) { fail ret.error; }\n    pass ret.value;', content)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
