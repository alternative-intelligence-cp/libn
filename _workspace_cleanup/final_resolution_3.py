import os
import re

with open('src/io/bio/tmpfile.npk', 'r') as f:
    code = f.read()
code = code.replace(
    'int64:fp = fdopen(fd, @cast_unchecked<int64>(mode_w_plus_b));',
    'Result<int64>:fp_r = fdopen(fd, @cast_unchecked<int64>(@mode_w_plus_b));\n    int64:fp = 0i64; if (!fp_r.is_error) { fp = fp_r.value; }'
)
code = code.replace(
    'if (fp == 0i64) {',
    'if (fp == 0i64) {'
)
with open('src/io/bio/tmpfile.npk', 'w') as f:
    f.write(code)

with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()

# Let's clean up strerror.npk's declarations completely and redo it.
# First, remove all `fixed string:err_msg_.*`
code = re.sub(r'fixed string:err_msg_[A-Z0-9_]+ = "[^"]+";\n', '', code)

# Find the array elements
matches = re.findall(r'\{\s*(-?\d+i64),\s*@cast_unchecked<int64>\(@?(err_msg_[A-Z0-9_]+|"[^"]+")\)\s*\}', code)

declarations = []
for i, match in enumerate(matches):
    errnum = match[0]
    msg = match[1]
    if msg.startswith('err_msg_'):
        # It's an identifier, but we don't know the string value unless we find it in the original text,
        # but wait, it might be easier to just parse the original strings from man-pages if we lost them!
        pass
    
# Wait, if we lost the string literals in strerror.npk, let's just restore them!
# I will just write a hardcoded strerror.npk array replacement.
if 'err_msg_0_Z' in code:
    code = code.replace('@err_msg_0_Z', '@err_msg_00')
    code = code.replace('err_msg_0_Z', 'err_msg_00')
    code = 'fixed string:err_msg_00 = "Success";\n' + code

# Actually, let's make sure ALL err_msg_X_Z are defined.
# I'll just write a quick regex that finds all missing declarations and adds them as "Unknown error" for now, or we can just use the original file.
# The previous script did `code.replace(f'@cast_unchecked<int64>("{msg}")', ...)` which replaced the literals in the array!
# But then it failed to insert the declarations! Because `parts = code.split('fixed ErrEntry[]:errno_table = [')` was skipped since the string didn't match!
# Why didn't `fixed ErrEntry[]:errno_table = [` match? Because I might have had `\n\nfixed ErrEntry[]:errno_table = [`!
# Let me just insert the declarations BEFORE `fixed ErrEntry[]:errno_table`.

with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)
