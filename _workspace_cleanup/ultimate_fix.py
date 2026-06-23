import os
import re

# 1. Revert strerror.npk array syntax to the working one
with open('src/io/bio/strerror.npk', 'r') as f:
    code = f.read()
code = code.replace('fixed ErrEntry:errno_table[] = [', 'fixed ErrEntry[]:errno_table = [')
with open('src/io/bio/strerror.npk', 'w') as f:
    f.write(code)

# 2. Fix the "Cannot cast 'FILE' to 'FILE@'" in stdfiles.npk
# g_stdin_file is probably already an int64 pointer?
# Let's check stdfiles.npk manually with a later command, for now, replace @g_stdin_file back to g_stdin_file if it's broken
with open('src/io/bio/stdfiles.npk', 'r') as f:
    code = f.read()
code = code.replace('(@g_stdin_file)', '(g_stdin_file)')
code = code.replace('(@g_stdout_file)', '(g_stdout_file)')
code = code.replace('(@g_stderr_file)', '(g_stderr_file)')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(code)

# 3. strfmt.npk: "Cannot index non-array type 'string'"
with open('src/str/strfmt.npk', 'r') as f:
    code = f.read()
code = code.replace('@"0123456789abcdef"[0]', '@LOWER_STR')
code = code.replace('@"0123456789ABCDEF"[0]', '@UPPER_STR')
code = code.replace('@"(null)"[0]', '@NULL_STR')
with open('src/str/strfmt.npk', 'w') as f:
    f.write(code)

# 4. strconv.npk: Undefined identifier 'errno_clear'
with open('src/str/strconv.npk', 'r') as f:
    code = f.read()
code = code.replace('errno_clear()', 'libn_errno_set(0i64)')
with open('src/str/strconv.npk', 'w') as f:
    f.write(code)

# 5. strlen.npk: Undefined identifier 'has_nul_byte'
with open('src/str/strlen.npk', 'r') as f:
    code = f.read()
code = code.replace('has_nul_byte', 'has_zero_byte')
with open('src/str/strlen.npk', 'w') as f:
    f.write(code)

# 6. fio.npk and fprintf.npk: Fix bio_flush_write_buf missing raw
# Wait, fio.npk: Result<int64>:r = bio_flush_write_buf(fp) -> it still fails?
print("Applied ultimate_fix.py")
