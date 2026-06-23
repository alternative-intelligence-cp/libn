import os
import re

files_to_fix = [
    # slab.npk
    ('src/mem/slab.npk', r'int64:sz\s+=\s+slab_class_size\((.*?)\);', r'int64:sz   = raw(slab_class_size(\1));'),
    # fstr.npk
    ('src/io/bio/fstr.npk', r'int64:c = fgetc\((.*?)\);', r'int64:c = raw(fgetc(\1));'),
    ('src/io/bio/fstr.npk', r'int64:c = fputc\((.*?)\);', r'int64:c = raw(fputc(\1));'),
    # fstate.npk
    ('src/io/bio/fstate.npk', r'int64:newbuf = bio_alloc_buf\((.*?)\);', r'int64:newbuf = raw(bio_alloc_buf(\1));'),
]

for file_path, pat, repl in files_to_fix:
    full_path = os.path.join('/home/randy/Workspace/REPOS/libn', file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            content = f.read()
        new_content = re.sub(pat, repl, content)
        if new_content != content:
            with open(full_path, 'w') as f:
                f.write(new_content)
            print(f"Fixed {file_path}")
