import os

def fix():
    # 1. strconv.npk
    path = "/home/randy/Workspace/REPOS/libn/src/str/strconv.npk"
    with open(path, "r") as f: content = f.read()

    # Replace endptr_val array with simple variable
    content = content.replace("stack int64[1]:endptr_val;\n    endptr_val[0] = s;\n    int64->:ep = @cast_unchecked<int64->>(@endptr_val[0]);",
                              "int64:endptr_val_0 = s;\n    int64->:ep = @cast_unchecked<int64->>(@endptr_val_0);")

    # Fix pointer dereference in array access
    content = content.replace("ep[0] != 0i64", "(raw ep[0]) != 0i64")
    content = content.replace("(@cast_unchecked<uint8->>(ep[0]))[0]", "(@cast_unchecked<uint8->>(raw ep[0]))[0]")
    
    # Fix str_strtol and libn_errno_get Result unwrapping
    content = content.replace("int64:v = str_strtol(", "int64:v = raw str_strtol(")
    content = content.replace("int64:v = str_strtoul(", "int64:v = raw str_strtoul(")
    content = content.replace("libn_errno_get() == ERANGE", "raw libn_errno_get() == ERANGE")
    with open(path, "w") as f: f.write(content)

    # 2. stdfiles.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/stdfiles.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("stdin_fp = bio_alloc_file();", "stdin_fp = raw bio_alloc_file();")
    content = content.replace("stdout_fp = bio_alloc_file();", "stdout_fp = raw bio_alloc_file();")
    content = content.replace("stderr_fp = bio_alloc_file();", "stderr_fp = raw bio_alloc_file();")
    with open(path, "w") as f: f.write(content)

    # 3. fstr.npk
    path = "/home/randy/Workspace/REPOS/libn/src/io/bio/fstr.npk"
    with open(path, "r") as f: content = f.read()
    content = content.replace("int64:len = str_strlen(s);", "int64:len = raw str_strlen(s);")
    content = content.replace("int64:c = fputc(", "int64:c = raw fputc(")
    with open(path, "w") as f: f.write(content)

fix()
