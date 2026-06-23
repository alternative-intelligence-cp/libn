import os
import re

def fix():
    # 1. fscanf.npk fixes
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fscanf.npk"
    with open(path, "r") as f: content = f.read()
    
    # Fix array casts that look like @cast_unchecked<int64@>(argv) or consumed
    content = re.sub(r'@cast_unchecked<int64@?>\(argv\)', '@cast_unchecked<int64>(@argv[0])', content)
    content = re.sub(r'@cast_unchecked<int64@?>\(consumed\)', '@cast_unchecked<int64>(@consumed[0])', content)
    content = re.sub(r'@cast_unchecked<int64>\(argv\)', '@cast_unchecked<int64>(@argv[0])', content)
    content = re.sub(r'@cast_unchecked<int64>\(consumed\)', '@cast_unchecked<int64>(@consumed[0])', content)
    
    with open(path, "w") as f: f.write(content)

    # 2. fprintf.npk fixes
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fprintf.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'@cast_unchecked<int64>\(buf\)', r'@cast_unchecked<int64>(@buf[0])', content)
    content = re.sub(r'@cast_unchecked<int64>\(tmp\)', r'@cast_unchecked<int64>(@tmp[0])', content)
    with open(path, "w") as f: f.write(content)

    # 3. strerror.npk fixes
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/strerror.npk"
    with open(path, "r") as f: content = f.read()
    # uint8->:dst = @cast_unchecked<uint8->>(g_strerror_unknown_buf); -> @g_strerror_unknown_buf[0]
    content = content.replace(
        "@cast_unchecked<uint8->>(g_strerror_unknown_buf)",
        "@cast_unchecked<uint8->>(@g_strerror_unknown_buf[0])"
    )
    # int64:msg = raw strerror(libn_errno); -> libn_errno_get()
    content = content.replace("libn_errno", "libn_errno_get()")
    # Wait, the comment says "Reads the current global errno value (libn_errno from errno.npk)."
    # But replacing libn_errno with libn_errno_get() in the code block is safe.
    # To be safe, let's only replace it where it's used as a variable.
    content = content.replace("raw strerror(libn_errno)", "raw strerror(libn_errno_get())")
    
    with open(path, "w") as f: f.write(content)

fix()
