import os

def fix():
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
    with open(path, "r") as f: content = f.read()

    # Add missing imports if not present
    if "mmap.npk" not in content:
        content = content.replace('use "src/mem/memutil.npk".*;', 'use "src/mem/memutil.npk".*;\nuse "src/mem/mmap.npk".*;\nuse "src/mem/memcpy.npk".*;')

    # Fix unwraps and typos
    content = content.replace("int64:len = str_snprintf", "int64:len = raw str_snprintf")
    content = content.replace("int64:p = mem_malloc", "int64:p = raw mem_malloc")
    content = content.replace("mem_memcpy(p", "drop mem_memcpy(p")
    # Actually asprintf uses str_snprintf, not memcpy? Wait! The error said "mem_memcpy(p, tmp, len+1)".
    content = content.replace("mem_memcpy(p, tmp, len + 1i64)", "drop mem_memcpy(p, tmp, len + 1i64)")
    
    # Fix bio_alloc_file
    content = content.replace("@cast_unchecked<int64>(bio_alloc_file())", "raw bio_alloc_file()")
    
    with open(path, "w") as f: f.write(content)
fix()
