import os, glob, re

# 1. Rename slab_alloc to mem_slab_alloc
for filepath in glob.glob('src/**/*.npk', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'slab_alloc' in content:
        content = re.sub(r'\bslab_alloc\b', 'mem_slab_alloc', content)
        with open(filepath, 'w') as f:
            f.write(content)

# 2. Fix stdfiles.npk
stdfiles = 'src/io/bio/stdfiles.npk'
if os.path.exists(stdfiles):
    with open(stdfiles, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'int64:r = fputs(s, stdout_fp);\n    if (r == FILE_EOF) {',
        'Result<int64>:r = fputs(s, stdout_fp);\n    if (r.is_error) { pass FILE_EOF; }\n    if (r.value == FILE_EOF) {'
    )
    
    content = content.replace(
        '''    int64:r1 = fflush(stdin_fp);
    int64:r2 = fflush(stdout_fp);
    int64:r3 = fflush(stderr_fp);
    if (r1 == FILE_EOF || r2 == FILE_EOF || r3 == FILE_EOF) {''',
        '''    Result<int64>:r1 = fflush(stdin_fp);
    Result<int64>:r2 = fflush(stdout_fp);
    Result<int64>:r3 = fflush(stderr_fp);
    int64:v1 = 0i64; if (!r1.is_error) { v1 = r1.value; } else { v1 = FILE_EOF; }
    int64:v2 = 0i64; if (!r2.is_error) { v2 = r2.value; } else { v2 = FILE_EOF; }
    int64:v3 = 0i64; if (!r3.is_error) { v3 = r3.value; } else { v3 = FILE_EOF; }
    if (v1 == FILE_EOF || v2 == FILE_EOF || v3 == FILE_EOF) {'''
    )
    
    with open(stdfiles, 'w') as f:
        f.write(content)

print("Fixes applied.")
