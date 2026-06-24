import re

def fix_fscanf():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/fscanf.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace('int64:c = bio_scan_getc(src);', 'int64:c = raw bio_scan_getc(src);')
    content = content.replace('c = bio_scan_getc(src);', 'c = raw bio_scan_getc(src);')
    content = content.replace('int64:next = bio_scan_getc(src);', 'int64:next = raw bio_scan_getc(src);')
    content = content.replace('int64:c = raw bio_scan_skip_ws(src);', 'int64:c = raw bio_scan_skip_ws(src);')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_file():
    path = '/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace('libn_slab_free(0i64, fp)', 'libn_slab_free(fp)')
    content = content.replace('libn_slab_free(0i64, buf)', 'libn_slab_free(buf)')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_memutil():
    path = '/home/randy/Workspace/REPOS/libn/src/mem/memutil.npk'
    with open(path, 'r') as f:
        content = f.read()
    
    # bad_char[0] = nlen;
    content = content.replace('bad_char[0] = nlen;', 'bad_char[0] = @cast_unchecked<uint16>(nlen);')
    # bad_char[i] = nlen;
    content = content.replace('bad_char[i] = nlen;', 'bad_char[i] = @cast_unchecked<uint16>(nlen);')
    # bad_char[@cast_unchecked<int64>(n[i])] = nlen - 1i64 - i;
    content = content.replace('bad_char[@cast_unchecked<int64>(n[i])] = nlen - 1i64 - i;', 'bad_char[@cast_unchecked<int64>(n[i])] = @cast_unchecked<uint16>(nlen - 1i64 - i);')
    
    with open(path, 'w') as f:
        f.write(content)

fix_fscanf()
fix_file()
fix_memutil()
