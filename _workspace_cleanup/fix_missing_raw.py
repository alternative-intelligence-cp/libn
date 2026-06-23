import os
import re

files_to_fix = [
    # fopen.npk
    ('src/io/bio/fopen.npk', r'int64:parse_ok = raw\(bio_parse_mode', r'int64:parse_ok = bio_parse_mode'),
    ('src/io/bio/fopen.npk', r'int64:fp = raw\(bio_alloc_file\(\)\)', r'int64:fp = bio_alloc_file()'),
    ('src/io/bio/fopen.npk', r'int64:parse_ok = bio_parse_mode\((.*?)\);', r'int64:parse_ok = raw(bio_parse_mode(\1));'),
    ('src/io/bio/fopen.npk', r'int64:fp = bio_alloc_file\(\);', r'int64:fp = raw(bio_alloc_file());'),
    
    # stdfiles.npk
    ('src/io/bio/stdfiles.npk', r'int64:stdin_buf = raw\(bio_alloc_buf\(BUFSIZ\)\)', r'int64:stdin_buf = bio_alloc_buf(BUFSIZ)'),
    ('src/io/bio/stdfiles.npk', r'int64:stdout_buf = raw\(bio_alloc_buf\(BUFSIZ\)\)', r'int64:stdout_buf = bio_alloc_buf(BUFSIZ)'),
    ('src/io/bio/stdfiles.npk', r'int64:r = raw\(fputs\(s, stdout_fp\)\)', r'int64:r = fputs(s, stdout_fp)'),
    ('src/io/bio/stdfiles.npk', r'int64:stdin_buf = bio_alloc_buf\((.*?)\);', r'int64:stdin_buf = raw(bio_alloc_buf(\1));'),
    ('src/io/bio/stdfiles.npk', r'int64:stdout_buf = bio_alloc_buf\((.*?)\);', r'int64:stdout_buf = raw(bio_alloc_buf(\1));'),
    ('src/io/bio/stdfiles.npk', r'int64:r = fputs\((.*?)\);', r'int64:r = raw(fputs(\1));'),
    
    # fio.npk
    ('src/io/bio/fio.npk', r'int64:newbuf = raw\(bio_alloc_buf', r'int64:newbuf = bio_alloc_buf'),
    ('src/io/bio/fio.npk', r'int64:newbuf = bio_alloc_buf\((.*?)\);', r'int64:newbuf = raw(bio_alloc_buf(\1));'),
    
    # fchar.npk
    ('src/io/bio/fchar.npk', r'int64:c = raw\(fgetc\(fp\)\)', r'int64:c = fgetc(fp)'),
    ('src/io/bio/fchar.npk', r'int64:c = fgetc\((.*?)\);', r'int64:c = raw(fgetc(\1));'),

    # slab.npk
    ('src/mem/slab.npk', r'int64:head = raw\(slab_freelist_get\(cls\)\)', r'int64:head = slab_freelist_get(cls)'),
    ('src/mem/slab.npk', r'int64:sz = raw\(mem_slab_class_to_size\(cls\)\)', r'int64:sz = mem_slab_class_to_size(cls)'),
    ('src/mem/slab.npk', r'int64:head = slab_freelist_get\((.*?)\);', r'int64:head = raw(slab_freelist_get(\1));'),
    ('src/mem/slab.npk', r'int64:sz = mem_slab_class_to_size\((.*?)\);', r'int64:sz = raw(mem_slab_class_to_size(\1));'),

    # syscall.npk
    ('src/syscall/syscall.npk', r'int64:ret = raw\(sys!!\(nr', r'int64:ret = sys!!(nr'),
    ('src/syscall/syscall.npk', r'int64:ret = raw\(sys!!!\(nr', r'int64:ret = sys!!!(nr'),
    ('src/syscall/syscall.npk', r'int64:ret = sys!!\((.*?)\);', r'int64:ret = raw(sys!!(\1));'),
    ('src/syscall/syscall.npk', r'int64:ret = sys!!!\((.*?)\);', r'int64:ret = raw(sys!!!(\1));'),
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
