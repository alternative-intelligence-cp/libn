import os
import glob
import re

def fix():
    # 1. file.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk"
    with open(path, "r") as f: content = f.read()
    # Replace @cast_unchecked<FILE->>(...) with ... => FILE->
    content = re.sub(r'@cast_unchecked<FILE->>\((.*?)\)', r'\1 => FILE->', content)
    # Fix slab_free
    content = content.replace("drop slab_free(", "drop mem_free(")
    with open(path, "w") as f: f.write(content)

    # 2. fopen.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("if (libn_fcntl(fd, F_GETFL, 0i64) & O_APPEND != 0i64) {", 
                              "if ((raw libn_fcntl(fd, F_GETFL, 0i64)) & O_APPEND != 0i64) {")
    content = re.sub(r'@cast_unchecked<FILE->>\((.*?)\)', r'\1 => FILE->', content)
    with open(path, "w") as f: f.write(content)

    # 3. fseek.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fseek.npk"
    with open(path, "r") as f: content = f.read()
    content = re.sub(r'@cast_unchecked<FILE->>\((.*?)\)', r'\1 => FILE->', content)
    with open(path, "w") as f: f.write(content)

    # 4. Find the file with the line 411 error
    for root, dirs, files in os.walk("/home/randy/Workspace/REPOS/libn/src"):
        for file in files:
            if file.endswith(".npk"):
                p = os.path.join(root, file)
                with open(p, "r") as f:
                    lines = f.readlines()
                    if len(lines) > 410:
                        line411 = lines[410]
                        if "= drop" in line411:
                            lines[410] = re.sub(r'^.* = drop (.*)', r'drop \1', line411)
                            with open(p, "w") as fw: fw.writelines(lines)
                        elif ":r = bio_" in line411: # if someone assigned a void bio_ function
                            lines[410] = re.sub(r'^.*:r = (bio_.*)', r'drop \1', line411)
                            with open(p, "w") as fw: fw.writelines(lines)

fix()
