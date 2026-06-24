import re

def fix_file(filename, replacements):
    with open(filename, 'r') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filename, 'w') as f:
        f.write(content)

fix_file('src/mem/mmap.npk', [
    ('int64:total = page_align_up(ALLOC_HEADER_SIZE + n);', 'int64:total = raw page_align_up(ALLOC_HEADER_SIZE + n);'),
    ('int64:new_total = page_align_up(ALLOC_HEADER_SIZE + new_size);', 'int64:new_total = raw page_align_up(ALLOC_HEADER_SIZE + new_size);')
])

fix_file('src/io/bio/fopen.npk', [
    ('int64:buf = bio_alloc_buf(BUFSIZ);', 'int64:buf = raw bio_alloc_buf(BUFSIZ);'),
    ('int64:parse_ok = bio_parse_mode(mode, FILE_MODE_PTR, O_FLAGS_PTR);', 'int64:parse_ok = raw bio_parse_mode(mode, FILE_MODE_PTR, O_FLAGS_PTR);'),
    ('int64:fp = bio_alloc_file();', 'int64:fp = raw bio_alloc_file();')
])

fix_file('src/io/bio/tmpfile.npk', [
    ('int64:entropy = tmpfile_get_entropy();', 'int64:entropy = raw tmpfile_get_entropy();')
])

print("Fixed raws!")
