import re

with open('/home/randy/Workspace/REPOS/libn/src/syscall/syscall.npk', 'r') as f:
    content = f.read()

content = content.replace('if (ptr->is_error)', 'if (r.is_error)')
content = content.replace('int64:n = ptr->value;', 'int64:n = r.value;')
content = content.replace('if (fd == 0i64) {', 'if (n == 0i64) {')
content = content.replace('total = total + fd;', 'total = total + n;')
content = content.replace('ptr = ptr + fd;', 'ptr = ptr + n;')
content = content.replace('remaining = remaining - fd;', 'remaining = remaining - n;')

# Wait! There are OTHER errors in syscall.npk!
# Let's fix them too!
content = content.replace('Result<int64>:r = sys', 'int64:r = raw sys')
content = content.replace('r.is_error', 'false') # Wait, NO!
# If it's `raw sys3`, it CANNOT fail!
# But `sys` functions DO fail, that's why they are wrapped in Result!
# Wait, `Result<int64>:r = sys3(...)` IS CORRECT!
# Why did it error on `Line 113: Cannot silently unwrap Result<int64> into 'r' of type 'int64'`?
# Because `sys1(...)` returns `Result<int64>`, but it's assigned to `int64:r`!

# Let's see:
