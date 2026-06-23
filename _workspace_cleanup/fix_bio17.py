import os
import re

def fix():
    # Fix SYS_READ, SYS_WRITE, SYS_LSEEK in all .npk files in io/bio
    for root, dirs, files in os.walk("/home/randy/Workspace/REPOS/libn/src/io/bio"):
        for file in files:
            if file.endswith(".npk"):
                p = os.path.join(root, file)
                with open(p, "r") as f:
                    content = f.read()
                content = content.replace("sys(SYS_READ,", "sys(READ,")
                content = content.replace("sys(SYS_WRITE,", "sys(WRITE,")
                content = content.replace("sys(SYS_LSEEK,", "sys(LSEEK,")
                content = content.replace("libn_errno_set(@cast_unchecked<int64>(r.error));", "drop libn_errno_set(@cast_unchecked<int64>(r.error));")
                # Fix fseek.npk int64:p = ftell(fp);
                content = content.replace("int64:p = ftell(fp);", "int64:p = raw ftell(fp);")
                # Fix fopen.npk int64:r = bio_flush_write_buf(fp);
                content = content.replace("int64:r = bio_flush_write_buf(fp);", "int64:r = raw bio_flush_write_buf(fp);")
                with open(p, "w") as f:
                    f.write(content)

fix()
