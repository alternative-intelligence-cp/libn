import os
import re

def patch_file(path, replacements):
    try:
        with open(path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return
    
    orig = content
    for old, new in replacements:
        content = content.replace(old, new)
        
    if orig != content:
        with open(path, 'w') as f:
            f.write(content)

def fix_all_cast_typos(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith('.npk'):
                path = os.path.join(dirpath, name)
                with open(path, 'r') as f:
                    content = f.read()
                if '@@cast_unchecked' in content:
                    content = content.replace('@@cast_unchecked', '@cast_unchecked')
                    with open(path, 'w') as f:
                        f.write(content)

def main():
    src_dir = '/home/randy/Workspace/REPOS/libn/src'
    
    # 1. Fix missing pub in file.npk
    file_npk = os.path.join(src_dir, 'io/bio/file.npk')
    patch_file(file_npk, [
        ('func:bio_alloc_file', 'pub func:bio_alloc_file'),
        ('func:bio_free_file', 'pub func:bio_free_file'),
        ('func:bio_alloc_buf', 'pub func:bio_alloc_buf'),
        ('func:bio_free_buf', 'pub func:bio_free_buf'),
        ('func:bio_flush_write_buf', 'pub func:bio_flush_write_buf'),
        ('func:bio_discard_read_buf', 'pub func:bio_discard_read_buf'),
        ('func:bio_refill_read_buf', 'pub func:bio_refill_read_buf'),
        ('func:bio_parse_mode', 'pub func:bio_parse_mode')
    ])
    
    # 2. Fix missing imports in fprintf.npk and others
    fprintf_npk = os.path.join(src_dir, 'io/bio/fprintf.npk')
    patch_file(fprintf_npk, [
        ('use "src/mem/slab.npk".*;\n', 'use "src/mem/slab.npk".*;\nuse "src/mem/mmap.npk".*;\nuse "src/mem/memcpy.npk".*;\n')
    ])
    
    # Add syscall_numbers.npk to files missing it
    for missing_syscall_import in ['io/bio/fio.npk', 'io/bio/file.npk', 'io/bio/fchar.npk', 'io/bio/fseek.npk']:
        p = os.path.join(src_dir, missing_syscall_import)
        patch_file(p, [
            ('use "src/syscall/errno.npk".*;\n', 'use "src/syscall/errno.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;\n')
        ])

    # 3. Fix Result unwraps
    patch_file(os.path.join(src_dir, 'io/bio/stdfiles.npk'), [
        ('int64:r1 = fflush(stdin_fp);', 'int64:r1 = raw fflush(stdin_fp);'),
        ('int64:r2 = fflush(stdout_fp);', 'int64:r2 = raw fflush(stdout_fp);'),
        ('int64:r3 = fflush(stderr_fp);', 'int64:r3 = raw fflush(stderr_fp);')
    ])
    
    patch_file(os.path.join(src_dir, 'mem/slab.npk'), [
        ('int64:cls = slab_class_for_size(n);', 'int64:cls = raw slab_class_for_size(n);'),
        ('int64:cls  = slab_class_for_size(n);', 'int64:cls  = raw slab_class_for_size(n);'),
        ('int64:old_head = slab_freelist_get(cls);', 'int64:old_head = raw slab_freelist_get(cls);')
    ])
    
    patch_file(os.path.join(src_dir, 'mem/memutil.npk'), [
        ('int64:tword = replicate_byte(c);', 'int64:tword = raw replicate_byte(c);')
    ])
    
    patch_file(os.path.join(src_dir, 'mem/mmap.npk'), [
        ('int64:new_total = page_align_up(ALLOC_HEADER_SIZE + new_size);', 'int64:new_total = raw page_align_up(ALLOC_HEADER_SIZE + new_size);')
    ])
    
    patch_file(os.path.join(src_dir, 'io/bio/fseek.npk'), [
        ('int64:p = ftell(fp);', 'int64:p = raw ftell(fp);')
    ])
    
    patch_file(os.path.join(src_dir, 'io/bio/file.npk'), [
        ('int64:p = slab_alloc_zero(80i64);', 'int64:p = raw slab_alloc_zero(80i64);')
    ])
    
    patch_file(os.path.join(src_dir, 'proc/exec.npk'), [
        ('int64:ret = execve(', 'int64:ret = raw execve(')
    ])

    # 4. Revert syscall.npk bad changes (actually just remove them, the file is tracked in git so we can just checkout)
    
    # 5. Fix @@cast_unchecked typos across all files
    fix_all_cast_typos(src_dir)

if __name__ == '__main__':
    main()
