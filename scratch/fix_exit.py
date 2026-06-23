import re

with open('src/proc/exit.npk', 'r') as f:
    content = f.read()

# Fix arrays
content = re.sub(r'int64:_atexit_handlers\[32\];', r'int64[32]:_atexit_handlers;', content)
content = re.sub(r'int64:_atqexit_handlers\[32\];', r'int64[32]:_atqexit_handlers;', content)

# Fix while loop conditions
content = re.sub(r'while i >= 0i64 \{', r'while (i >= 0i64) {', content)

# Fix if conditions
content = re.sub(r'if _atexit_count >= ATEXIT_MAX \{', r'if (_atexit_count >= ATEXIT_MAX) {', content)
content = re.sub(r'if _atqexit_count >= ATEXIT_MAX \{', r'if (_atqexit_count >= ATEXIT_MAX) {', content)
content = re.sub(r'if fn != 0i64 \{', r'if (fn != 0i64) {', content)

# Fix pass statements
content = re.sub(r'pass -1i64;', r'pass(-1i64);', content)
content = re.sub(r'pass 0i64;', r'pass(0i64);', content)

# Fix call fn()
call_replace = """            (void)():f = @cast_unchecked<(void)()>(fn);
            f();"""
content = re.sub(r'            call fn\(\);', call_replace, content)

# Fix function ending braces
content = re.sub(r'^\}(?!\;)', r'};', content, flags=re.MULTILINE)

with open('src/proc/exit.npk', 'w') as f:
    f.write(content)
