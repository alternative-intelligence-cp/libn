import os
import re

filepath = 'src/syscall/syscall.npk'
with open(filepath, 'r') as f:
    code = f.read()

import re

# Replace sys_safe implementation using regex since the text changes
code = re.sub(r'Result<int64>:ret = sys\(nr, a1, a2, a3, a4, a5, a6\);\s*pass ret;',
              r'''int64:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (ret > -4096i64 && ret < 0i64) {
        fail @cast_unchecked<int64>(0i64 - ret);
    }
    pass raw ret;''', code)

# Replace sys_full implementation
code = re.sub(r'Result<int64>:ret = sys!!\(nr, a1, a2, a3, a4, a5, a6\);\s*pass ret;',
              r'''int64:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (ret > -4096i64 && ret < 0i64) {
        fail @cast_unchecked<int64>(0i64 - ret);
    }
    pass raw ret;''', code)

with open(filepath, 'w') as f:
    f.write(code)

