import re

path = '/home/randy/Workspace/REPOS/libn/src/io/bio/file.npk'
with open(path, 'r') as f:
    content = f.read()

# Add pub to these bio internal functions
funcs = ['bio_parse_mode', 'bio_free_buf', 'bio_discard_read_buf', 'bio_alloc_buf', 'bio_alloc_file', 'bio_refill_read_buf', 'bio_free_file']

for func in funcs:
    content = re.sub(rf'\nfunc:{func} =', rf'\npub func:{func} =', content)

with open(path, 'w') as f:
    f.write(content)

# Add ERR_EOF to errno.npk
errno_path = '/home/randy/Workspace/REPOS/libn/src/syscall/errno.npk'
with open(errno_path, 'r') as f:
    errno_content = f.read()

if 'ERR_EOF' not in errno_content:
    errno_content = errno_content.replace('pub fixed int64:ERR_BADARG      = 201i64;    // libn: bad argument\n', 'pub fixed int64:ERR_BADARG      = 201i64;    // libn: bad argument\npub fixed int64:ERR_EOF         = 202i64;    // libn: unexpected EOF\n')

# Add errno_clear to errno.npk
if 'errno_clear' not in errno_content:
    errno_content += '\n// errno_clear — Clear the error code\npub func:errno_clear = NIL() { drop libn_errno_set(0i64); };\n'

with open(errno_path, 'w') as f:
    f.write(errno_content)

print("Fixed bio visibility and errno")
