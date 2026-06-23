import os, glob

# 1. syscall.npk
syscall_path = 'src/syscall/syscall.npk'
if os.path.exists(syscall_path):
    with open(syscall_path, 'r') as f:
        content = f.read()
    
    # sys_safe and sys_full both have:
    old_sys = '''    int64:ret = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (ret > -4096i64 && ret < 0i64) {
        fail @cast_unchecked<int64>(0i64 - ret);
    }
    pass raw ret;'''
    new_sys = '''    Result<int64>:__r = sys!!(nr, a1, a2, a3, a4, a5, a6);
    if (__r.is_error) {
        fail @cast_unchecked<int64>(__r.error);
    }
    pass raw __r.value;'''
    
    content = content.replace(old_sys, new_sys)
    with open(syscall_path, 'w') as f:
        f.write(content)

# 2. Add `raw ` wrapper to specific files
replacements = {
    'src/mem/memutil.npk': [('int64:tword = replicate_byte(c);', 'int64:tword = raw replicate_byte(c);')],
    'src/mem/mmap.npk': [('int64:new_total = page_align_up(ALLOC_HEADER_SIZE + new_size);', 'int64:new_total = raw page_align_up(ALLOC_HEADER_SIZE + new_size);')],
    'src/mem/slab.npk': [
        ('int64:cls = slab_class_for_size(n);', 'int64:cls = raw slab_class_for_size(n);'),
        ('int64:old_head = slab_freelist_get(cls);', 'int64:old_head = raw slab_freelist_get(cls);'),
        ('int64:cls  = slab_class_for_size(n);', 'int64:cls  = raw slab_class_for_size(n);')
    ],
    'src/io/bio/fseek.npk': [('int64:p = ftell(fp);', 'int64:p = raw ftell(fp);')],
    'src/io/bio/fstr.npk': [
        ('int64:c = fgetc(fp);', 'int64:c = raw fgetc(fp);'),
        ('int64:c = fputc(@cast_unchecked<int64>(p[i]), fp);', 'int64:c = raw fputc(@cast_unchecked<int64>(p[i]), fp);')
    ],
    'src/io/bio/fscanf.npk': [
        ('int64:c = bio_scan_getc(src);', 'int64:c = raw bio_scan_getc(src);'),
        ('int64:c = bio_scan_skip_ws(src);', 'int64:c = raw bio_scan_skip_ws(src);')
    ]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old_str, new_str in reps:
            content = content.replace(old_str, new_str)
        with open(filepath, 'w') as f:
            f.write(content)

print("Type errors fixed.")
