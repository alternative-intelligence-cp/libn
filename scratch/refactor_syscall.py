import re

with open('src/syscall/syscall.npk', 'r') as f:
    content = f.read()

content = content.replace("(_) {", "(*) {")

ptr_args = ['path', 'buf', 'addr', 'old_addr', 'new_addr', 'uaddr', 'statxbuf', 'tidptr', 'ts_req']

lines = content.split('\n')
for i, line in enumerate(lines):
    # If this is a signature line, we ONLY change int64:X to any->:X
    if 'pub func:' in line:
        for arg in ptr_args:
            line = re.sub(rf'\bint64:{arg}\b', f'any->:{arg}', line)
        lines[i] = line
    else:
        # It's a body line, replace the argument inside sysX calls
        # We know they are passed as `arg,` or `arg)`
        if 'sys' in line or 'int64:ptr =' in line:
            for arg in ptr_args:
                # We need to make sure we match the exact word.
                line = re.sub(rf'\b{arg}\b([,\)])', rf'@cast_unchecked<int64>({arg})\1', line)
            
            # Special case for ptr assignment
            line = line.replace('int64:ptr = @cast_unchecked<int64>(buf);', 'uint8->:ptr = @cast_unchecked<uint8->>(buf);')
            
            lines[i] = line

content = '\n'.join(lines)

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(content)
