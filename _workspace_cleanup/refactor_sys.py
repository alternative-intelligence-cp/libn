import re

with open("src/syscall/syscall.npk", "r") as f:
    text = f.read()

def replacer(m):
    full_match = m.group(0)
    args_str = m.group(1)
    args = [a.strip() for a in args_str.split(',')]
    
    # Pad to 7 args
    while len(args) < 7:
        args.append("0i64")
    
    new_args = ", ".join(args)
    
    if "full" in full_match:
        func = "sys!!"
    elif "raw" in full_match:
        func = "sys!!!"
    else:
        func = "sys"
        
    return f"{func}({new_args})"

# Match sys_safe, sys1-sys6, sys_full, sys_full1-sys_full6, sys_raw
pattern = r'\bsys(?:_safe|[1-6]|_full[1-6]?|_raw)\s*\(([^)]+)\)'

new_text = re.sub(pattern, replacer, text)

# Now delete the definitions of sys_safe etc.
# They are between lines 75 and 160. Let's just comment them out or remove them.
# The simplest way is a regex that removes `pub func:sys... { ... }` where it matches those exact functions.
# Since we are just removing lines 75 to 160:
lines = new_text.split('\n')
# Wait, we don't need to delete them if they aren't used, but they have invalid sys(nr) which will throw errors!
# Let's just delete lines 75 through 160.
new_lines = lines[:74] + lines[160:]
new_text = '\n'.join(new_lines)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(new_text)

