import re
import os

files_to_fix = [
    "src/syscall/errno.npk",
    "src/io/bio/tmpfile.npk",
    "src/proc/exec.npk",
    "src/io/bio/strerror.npk",
    "src/fs/path.npk",
    "src/proc/env.npk"
]

def str_to_byte_array(s):
    bytes_arr = [str(ord(c)) + "u8" for c in s]
    bytes_arr.append("0u8")
    return "[" + ", ".join(bytes_arr) + "]"

for fpath in files_to_fix:
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, "r") as f:
        content = f.read()

    # Find all occurrences of @cast_unchecked<*byte[]>(\@"..."[0])
    # or @cast_unchecked<int64>(\@"..."[0])
    # or pass "..." -> wait we changed errno to pass @cast_unchecked...
    # Let's match @cast_unchecked<(int64|\*byte\[\])>\(@?"([^"]+)"\[0\]\)
    
    matches = re.finditer(r'@cast_unchecked<((?:int64)|(?:\*byte\[\]))>\(@?"([^"]+)"\[0\]\)', content)
    
    globals_to_add = []
    str_counter = 1
    
    # We process from bottom up so offsets don't change
    for m in reversed(list(matches)):
        cast_type = m.group(1)
        string_val = m.group(2)
        
        var_name = f"STR_{os.path.basename(fpath).split('.')[0].upper()}_{str_counter}"
        str_counter += 1
        
        byte_arr = str_to_byte_array(string_val)
        globals_to_add.append(f"fixed byte[]:{var_name} = {byte_arr};")
        
        # Replace the match with @cast_unchecked<cast_type>(@var_name[0])
        replacement = f"@cast_unchecked<{cast_type}>(@{var_name}[0])"
        content = content[:m.start()] + replacement + content[m.end():]
        
    if globals_to_add:
        # Insert globals after 'use' statements
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('use '):
                insert_idx = i + 1
        
        new_content = '\n'.join(lines[:insert_idx]) + '\n\n' + '\n'.join(globals_to_add) + '\n' + '\n'.join(lines[insert_idx:])
        with open(fpath, "w") as f:
            f.write(new_content)

