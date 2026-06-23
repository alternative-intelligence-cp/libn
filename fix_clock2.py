import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Replace `pass(errno_set(X));` with `drop errno_set(X); pass -1i64;`
    content = re.sub(r'pass\s*\(?\s*errno_set\((.*?)\)\s*\)?;', r'drop errno_set(\1); pass -1i64;', content)
    content = re.sub(r'pass\s+errno_set\((.*?)\);', r'drop errno_set(\1); pass -1i64;', content)

    # SYS_CLOCK_SETTIME is actually missing from posix_constants or syscalls? Let's check.
    # The error was "Unknown syscall constant 'CLOCK_SETTIME'" or "SYS_CLOCK_SETTIME"
    # Wait, earlier I changed it to SYS_CLOCK_SETTIME. If it still complains, we might need to add it.
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('/home/randy/Workspace/REPOS/libn/src/time/clock.npk')
fix_file('/home/randy/Workspace/REPOS/libn/src/time/timeofday.npk')
print("Fixed clock and timeofday pass errno_set")
