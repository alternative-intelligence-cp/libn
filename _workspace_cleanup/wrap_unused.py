import os
import re

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            content = re.sub(r'^(\s*)libn_errno_set\((.*?)\);', r'\1drop libn_errno_set(\2);', content, flags=re.MULTILINE)
            content = re.sub(r'^(\s*)slab_freelist_set\((.*?)\);', r'\1drop slab_freelist_set(\2);', content, flags=re.MULTILINE)
            content = re.sub(r'^(\s*)bio_flush_stdout\((.*?)\);', r'\1drop bio_flush_stdout(\2);', content, flags=re.MULTILINE)
            content = re.sub(r'^(\s*)bio_flush_all\((.*?)\);', r'\1drop bio_flush_all(\2);', content, flags=re.MULTILINE)
            content = re.sub(r'^(\s*)bio_ensure_std_init\((.*?)\);', r'\1drop bio_ensure_std_init(\2);', content, flags=re.MULTILINE)
            content = re.sub(r'^(\s*)libn_write\((.*?)\);', r'\1drop libn_write(\2);', content, flags=re.MULTILINE)
            
            with open(filepath, 'w') as f:
                f.write(content)
