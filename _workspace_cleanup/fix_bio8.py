import os
import re

def fix():
    # 1. strcmp.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strcmp.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("uint8:ca = to_lower_ascii(", "uint8:ca = raw to_lower_ascii(")
    content = content.replace("uint8:cb = to_lower_ascii(", "uint8:cb = raw to_lower_ascii(")
    with open(path, "w") as f: f.write(content)

    # 2. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()
    if "src/str/strcpy.npk" not in content:
        content = content.replace('use "src/str/strlen.npk".*;', 'use "src/str/strlen.npk".*;\nuse "src/str/strcpy.npk".*;')
    content = content.replace('str_strlen("-9223372036854775808")', 'raw str_strlen(@cast_unchecked<int64>("-9223372036854775808"))')
    content = content.replace('@cast_unchecked<int64>(@min_int)', '@cast_unchecked<int64>(min_int)')
    with open(path, "w") as f: f.write(content)

    # 3. mmap.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/mmap.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("libn_munmap(base, total_size)", "drop libn_munmap(base, total_size)")
    with open(path, "w") as f: f.write(content)

    # 4. memcpy.npk
    path = "/home/randy/Workspace/REPOS/libn/src/mem/memcpy.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("fail r;", "fail r.error;")
    content = content.replace("fail rc;", "fail rc.error;")
    with open(path, "w") as f: f.write(content)

    # 5. strfmt.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strfmt.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("@cast_unchecked<FmtState->>(st_arr)", "@cast_unchecked<FmtState->>(@st_arr[0])")
    content = content.replace("@cast_unchecked<int64>(nbuf)", "@cast_unchecked<int64>(@nbuf[0])")
    content = content.replace("@cast_unchecked<int64>(prefix)", "@cast_unchecked<int64>(@prefix[0])")
    # fmt_putc, fmt_puts_n, fmt_pad returns NIL, check if they are missing drop
    content = content.replace("fmt_putc(", "drop fmt_putc(")
    content = content.replace("fmt_puts_n(", "drop fmt_puts_n(")
    content = content.replace("fmt_pad(", "drop fmt_pad(")
    content = content.replace("drop drop ", "drop ")
    with open(path, "w") as f: f.write(content)

    # 6. file.npk missing drops? (bio_free_buf, bio_free_file)
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fopen.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("bio_free_buf(", "drop bio_free_buf(")
    content = content.replace("drop drop ", "drop ")
    with open(path, "w") as f: f.write(content)

    # 7. Add syscall numbers to tmpfile, fio, and fseek
    for f in ["tmpfile.npk", "fseek.npk", "fchar.npk"]:
        p = f"/home/randy/Workspace/REPOS/libn/src/io/bio/{f}"
        if not os.path.exists(p): continue
        with open(p, "r") as fd: c = fd.read()
        if "syscall_numbers.npk" not in c and "syscall.npk" in c:
            c = c.replace('use "src/syscall/syscall.npk".*;', 'use "src/syscall/syscall.npk".*;\nuse "src/syscall/syscall_numbers.npk".*;')
            with open(p, "w") as fd: fd.write(c)
            
fix()
