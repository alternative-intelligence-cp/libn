with open('src/time/sleep.npk', 'r') as f:
    content = f.read()

content = content.replace('pass(libn_errno_set(14i64));', 'drop libn_errno_set(14i64); pass -1i64;')
content = content.replace('pass(libn_errno_set(@cast_unchecked<int64>(r.error)));', 'drop libn_errno_set(@cast_unchecked<int64>(r.error)); pass -1i64;')
content = content.replace('SYS_NANOSLEEP', 'SYS_NANOSLEEP')

with open('src/time/sleep.npk', 'w') as f:
    f.write(content)
