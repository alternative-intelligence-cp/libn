import os
import re

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            # Fix func signatures
            content = re.sub(r'func:([A-Za-z0-9_]+)\s*=\s*Result<([A-Za-z0-9_@\[\]]+)>\(', r'func:\1 = \2(', content)

            # Fix .err to .error
            content = content.replace(".err", ".error")
            content = content.replace("fail r.erroror", "fail r.error")

            # Fix pass raw sys -> pass sys
            # Wait, if `libn_getpid = int64()`, we can just `pass sys(...)`?
            # NO! `sys(...)` returns `Result<int64>`. But the function signature `int64()` expects us to `pass` an `int64`!
            # If we `pass sys(...)`, we are passing `Result<int64>`, which wraps into `Result<Result<int64>>`!
            # So `pass raw sys(...)` is CORRECT! It extracts the `int64` from `Result<int64>` and passes it, which gets wrapped into `Result<int64>`!
            # BUT wait, what if `sys(...)` fails? `raw` will crash!
            # So we SHOULD NOT use `pass raw sys(...)`. We should do:
            # Result<int64>:r = sys(...); if (r.is_error) { fail r.error; } pass r.value;
            
            with open(filepath, 'w') as f:
                f.write(content)
