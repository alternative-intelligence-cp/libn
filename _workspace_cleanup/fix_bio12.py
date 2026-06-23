import re

def fix():
    # 1. file.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk"
    with open(path, "r") as f: content = f.read()
    
    content = re.sub(r'FILE->:([a-z0-9_]+) = ([a-z0-9_]+) => FILE->;', r'FILE->:\1 = @cast_unchecked<FILE->>(\2);', content)
    content = content.replace("slab_free(bio_file_slab, ", "slab_free(")
    content = content.replace("int64:p = slab_alloc_zero(", "int64:p = raw slab_alloc_zero(")
    if '"src/mem/mmap.npk"' not in content:
        content = content.replace('use "src/mem/slab.npk".*;\n', 'use "src/mem/slab.npk".*;\nuse "src/mem/mmap.npk".*;\n')
    
    with open(path, "w") as f: f.write(content)

    # 2. test_root.npk
    path = "/home/randy/Workspace/REPOS/libn/test_root.npk"
    with open(path, "r") as f: lines = f.readlines()
    
    for i in range(len(lines)):
        line = lines[i]
        if "int64:r = libn_read" in line:
            lines[i] = line.replace("int64:r = libn_read", "int64:r = raw libn_read")
        elif "int64:tword = libn_read" in line:
            lines[i] = line.replace("int64:tword = libn_read", "int64:tword = raw libn_read")
        elif "if (libn_lseek" in line:
            lines[i] = line.replace("libn_lseek", "raw libn_lseek")
        elif "= drop " in line:
            # line 411: cannot use the result of a void-returning function as an initializer
            lines[i] = re.sub(r'^[ \t]*([a-zA-Z0-9_<>\:]+) = drop (.*);', r'drop \2;', line)
        elif "int64:r = drop " in line or "Result<int64>:r = drop " in line:
            lines[i] = re.sub(r'.* = drop (.*);', r'drop \1;', line)
            
    with open(path, "w") as f: f.writelines(lines)

fix()
