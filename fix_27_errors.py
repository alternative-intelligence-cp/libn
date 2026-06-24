import re

def fix_file(path, replacements):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    for line_idx, src, dest in replacements:
        line_idx -= 1
        lines[line_idx] = lines[line_idx].replace(src, dest)
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')

fix_file('src/mem/mmap.npk', [
    (196, 'int64:total = page_align_up', 'int64:total = raw page_align_up'),
    (299, 'int64:new_total = page_align_up', 'int64:new_total = raw page_align_up')
])

fix_file('src/io/bio/fopen.npk', [
    (116, 'int64:parse_ok = bio_parse_mode', 'int64:parse_ok = raw bio_parse_mode'),
    (134, 'int64:fp = bio_alloc_file', 'int64:fp = raw bio_alloc_file'),
    (178, 'int64:parse_ok = bio_parse_mode', 'int64:parse_ok = raw bio_parse_mode'),
    (184, 'int64:fp = bio_alloc_file', 'int64:fp = raw bio_alloc_file'),
    (225, 'int64:parse_ok = bio_parse_mode', 'int64:parse_ok = raw bio_parse_mode')
])

fprintf_fixes = []
for line in [72, 94, 116, 138, 161, 184, 210, 238, 266, 301, 312, 323, 335, 347]:
    fprintf_fixes.append((line, 'int64:len = str_snprintf', 'int64:len = raw str_snprintf'))
fix_file('src/io/bio/fprintf.npk', fprintf_fixes)

fix_file('src/io/bio/tmpfile.npk', [
    (119, 'int64:tmpl_len = str_strlen', 'int64:tmpl_len = raw str_strlen'),
    (143, 'int64:entropy = tmpfile_get_entropy', 'int64:entropy = raw tmpfile_get_entropy'),
    (183, 'int64:tmpl_len = str_strlen', 'int64:tmpl_len = raw str_strlen'),
    (202, 'int64:entropy = tmpfile_get_entropy', 'int64:entropy = raw tmpfile_get_entropy'),
    (242, 'int64:pfx_len = str_strlen', 'int64:pfx_len = raw str_strlen'),
    (246, 'int64:fd = mkstemp', 'int64:fd = raw mkstemp')
])
