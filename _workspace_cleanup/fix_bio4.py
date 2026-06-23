import os
import re

bio_dir = "/home/randy/Workspace/REPOS/libn/src/io/bio"

def fix_last_errors():
    for root, _, files in os.walk(bio_dir):
        for filename in files:
            if not filename.endswith(".npk"): continue
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            
            original = content
            
            # 1. void -> NIL
            content = re.sub(r'\bvoid\(', 'NIL(', content)
            
            # 2. strerror.npk fixes
            if filename == "strerror.npk":
                content = content.replace(
                    "str_int64_to_dec(errnum, @cast_unchecked<int64>(num), 24i64)",
                    "raw str_itoa(errnum, @cast_unchecked<int64>(@num[0]), 24i64)"
                )
                content = content.replace(
                    "mem_memcpy(@cast_unchecked<int64>(dst) + prefix_len, @cast_unchecked<int64>(num), num_len + 1i64)",
                    "mem_memcpy(@cast_unchecked<int64>(dst) + prefix_len, @cast_unchecked<int64>(@num[0]), num_len + 1i64)"
                )
                content = content.replace(
                    "int64:msg = strerror(errnum)",
                    "int64:msg = raw strerror(errnum)"
                )
                content = content.replace(
                    "int64:msg_len = str_strlen(msg)",
                    "int64:msg_len = raw str_strlen(msg)"
                )
            
            # 3. tmpfile.npk fixes
            if filename == "tmpfile.npk":
                content = content.replace(
                    "dst = @g_tmpnam_buf[0] => int64;",
                    "dst = @cast_unchecked<int64>(@g_tmpnam_buf[0]);"
                )
            
            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed final errors in {filename}")

fix_last_errors()
