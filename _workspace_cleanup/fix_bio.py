import os
import re

bio_dir = "/home/randy/Workspace/REPOS/libn/src/io/bio"

# Regexes for pointer access replacements
f_dot_re = re.compile(r'\bf\.(fd|buf_pos|flags|buf_len|unget|mode|file_pos|buf_cap|buf_mode|buf)\b')

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Global replacements
    # 1. f.member -> f->member
    content = f_dot_re.sub(r'f->\1', content)

    # 2. byte: -> uint8:
    content = re.sub(r'\bbyte:', 'uint8:', content)
    
    # 3. sys_safe -> sys
    content = re.sub(r'\bsys_safe\(', 'sys(', content)

    # 4. fscanf.npk specific fixes
    if filepath.endswith("fscanf.npk"):
        content = content.replace("@cast_unchecked<int64>(src)", "@cast_unchecked<int64>(@src[0])")
        content = content.replace("@cast_unchecked<int64>(argv)", "@cast_unchecked<int64>(@argv[0])")
    
    # 4. tmpfile.npk specific fixes
    if filepath.endswith("tmpfile.npk"):
        content = content.replace("int64:tmpl_len = str_strlen(tmpl);", "int64:tmpl_len = raw str_strlen(tmpl);")
        content = content.replace("int64:entropy = tmpfile_get_entropy();", "int64:entropy = raw tmpfile_get_entropy();")
        content = content.replace("int64:pfx_len = str_strlen(pfx);", "int64:pfx_len = raw str_strlen(pfx);")
        content = content.replace("@tmpl => int64", "@cast_unchecked<int64>(@tmpl[0])")
        content = content.replace("@tmpl[0] => int64", "@cast_unchecked<int64>(@tmpl[0])")
        content = content.replace("@tmpl => wild uint8->", "@cast_unchecked<uint8->>(@tmpl[0])")

    # 5. Fix unused result from NIL-returning functions
    # As per audit: drop(write_temp_data(fd));
    # Actually wait, I shouldn't just regex this unless I know the exact lines.
    # The audit says: "Lines 127, 167, 176, 191, 231, 246, 593-636"
    # But wait, `tmpfile.npk` has `drop libn_errno_set(...)`. The audit says `drop(libn_errno_set(...))`.
    # Does `drop expr` work? Yes, `drop` is a keyword. I've already fixed the double drops.

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for root, _, files in os.walk(bio_dir):
    for filename in files:
        if filename.endswith(".npk"):
            process_file(os.path.join(root, filename))

