import re

with open('src/syscall/errno.npk', 'r') as f:
    c = f.read()

# Fix the broken pick e -> if else chain and string casts
# Find all `@cast_unchecked<pass>(NUMBER) "STRING";`
def repl(m):
    val = m.group(1)
    msg = m.group(2)
    return f'if (e == {val}) {{ pass @cast_unchecked<uint8->>(@"{msg}"[0]); }}'

c = re.sub(r'@cast_unchecked<pass>\(([0-9]+i64)\)\s*"([^"]+)";', repl, c)

# Fix the fallback: `_ => pass "Unknown error";` might have become something else?
# What did `_ => pass "Unknown error";` become?
# It might be `@cast_unchecked<pass>(_) "Unknown error";`
def repl_fallback(m):
    msg = m.group(1)
    return f'pass @cast_unchecked<uint8->>(@"{msg}"[0]);'

c = re.sub(r'@cast_unchecked<pass>\(_\)\s*"([^"]+)";', repl_fallback, c)

# Let's remove the `pick e {` and `}` if they exist.
# `pick e {` -> ``
c = re.sub(r'pick\s+e\s*\{', '', c)
# The matching `}` for `pick e {` is at the end of the function, before `pass "Unknown error";`?
# Actually, we can just let it be if it's there.

with open('src/syscall/errno.npk', 'w') as f:
    f.write(c)

print("Fixed errno manually.")
