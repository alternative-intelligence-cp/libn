import os
import re

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                code = f.read()

            modified = False

            # Replace `drop bio_ensure_std_init();` with `drop(bio_ensure_std_init());`
            if 'drop bio_ensure_std_init();' in code:
                code = code.replace('drop bio_ensure_std_init();', 'drop(bio_ensure_std_init());')
                modified = True

            # Replace `drop bio_flush_all();`
            if 'drop bio_flush_all();' in code:
                code = code.replace('drop bio_flush_all();', 'drop(bio_flush_all());')
                modified = True

            # Replace `drop bio_flush_write_buf(fp);`
            if 'drop bio_flush_write_buf(fp);' in code:
                code = code.replace('drop bio_flush_write_buf(fp);', 'drop(bio_flush_write_buf(fp));')
                modified = True

            # Replace `drop bio_discard_read_buf(fp);`
            if 'drop bio_discard_read_buf(fp);' in code:
                code = code.replace('drop bio_discard_read_buf(fp);', 'drop(bio_discard_read_buf(fp));')
                modified = True

            # Replace `drop str_snprintfX(...)`
            new_code = re.sub(r'drop\s+str_snprintf([0-8])\((.*?)\);', r'drop(str_snprintf\1(\2));', code)
            if new_code != code:
                code = new_code
                modified = True
                
            # Any remaining `Result<NIL>:_r_init = bio_ensure_std_init();`
            new_code = re.sub(r'Result<NIL>:_r_init\s*=\s*bio_ensure_std_init\(\);\s*(if\s*\(_r_init\.is_error\)\s*\{\s*\})?', r'drop(bio_ensure_std_init());', code)
            if new_code != code:
                code = new_code
                modified = True

            if modified:
                with open(filepath, 'w') as f:
                    f.write(code)

print("Applied ultimate_fixer16.py")
