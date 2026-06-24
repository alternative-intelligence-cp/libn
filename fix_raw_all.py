import os
import re

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            original = content

            # Fix tmpfile.npk specific issues
            content = content.replace("int64:tmpl_len = str_strlen", "int64:tmpl_len = raw str_strlen")
            content = content.replace("int64:pfx_len = str_strlen", "int64:pfx_len = raw str_strlen")
            content = content.replace("int64:entropy = sys_safe", "int64:entropy = raw sys_safe")
            
            # For libn_open in tmpfile:
            # int64:fd = libn_open(...)
            # if (fd < 0i64) { ... }
            content = re.sub(
                r'int64:fd = libn_open\((.*?)\);\n\s*if \(fd < 0i64\)',
                r'Result<int64>:fd_res = libn_open(\1);\n        if (fd_res.is_error)',
                content
            )
            # also replace `fd` with `fd_res.value` where needed right after?
            # actually, tmpfile.npk has `pass fd;` or similar
            
            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Updated {filepath}")
