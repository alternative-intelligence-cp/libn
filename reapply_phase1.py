import re
import os

# 1. src/str/strfmt.npk: remove lines 157-159 `if (buf == 0i64 || buf_size <= 0i64) { pass 0i64; }`
with open('src/str/strfmt.npk', 'r') as f:
    lines = f.readlines()
new_lines = []
skip = 0
for line in lines:
    if 'if (buf == 0i64 || buf_size <= 0i64) {' in line:
        skip = 3
    if skip > 0:
        skip -= 1
        continue
    new_lines.append(line)
with open('src/str/strfmt.npk', 'w') as f:
    f.writelines(new_lines)

# 2. src/io/bio/file.npk: add g_open_files
with open('src/io/bio/file.npk', 'r') as f:
    content = f.read()
content = content.replace('    int64:next_global;\n};\n', '    int64:next_global;\n};\n\npub int64:g_open_files = 0i64;\n')
with open('src/io/bio/file.npk', 'w') as f:
    f.write(content)

# 3. src/io/bio/fopen.npk: add f->next_global = g_open_files; g_open_files = fp; to fopen and fdopen
# also add unlink logic to fclose
with open('src/io/bio/fopen.npk', 'r') as f:
    content = f.read()

content = content.replace('    FILE->:f = @cast_unchecked<FILE->>(fp);\n    pass fp;\n};\n',
                          '    FILE->:f = @cast_unchecked<FILE->>(fp);\n    f->next_global = g_open_files;\n    g_open_files = fp;\n    pass fp;\n};\n')

unlink_code = """
    int64:prev = 0i64;
    int64:curr = g_open_files;
    while (curr != 0i64) {
        FILE->:c = @cast_unchecked<FILE->>(curr);
        if (curr == fp) {
            if (prev == 0i64) {
                g_open_files = c->next_global;
            } else {
                FILE->:p = @cast_unchecked<FILE->>(prev);
                p->next_global = c->next_global;
            }
            break;
        }
        prev = curr;
        curr = c->next_global;
    }
"""
content = content.replace('    FILE->:f = @cast_unchecked<FILE->>(fp);\n    int64:ret = 0i64;',
                          f'    FILE->:f = @cast_unchecked<FILE->>(fp);\n{unlink_code}\n    int64:ret = 0i64;')
with open('src/io/bio/fopen.npk', 'w') as f:
    f.write(content)

# 4. src/io/bio/stdfiles.npk: link std streams
with open('src/io/bio/stdfiles.npk', 'r') as f:
    content = f.read()
content = content.replace('    stderr_fp = @cast_unchecked<int64>(@g_stderr_file);\n};',
                          '    stderr_fp = @cast_unchecked<int64>(@g_stderr_file);\n    sout->next_global = g_open_files;\n    g_open_files = stdout_fp;\n    sin->next_global = g_open_files;\n    g_open_files = stdin_fp;\n    serr->next_global = g_open_files;\n    g_open_files = stderr_fp;\n};')
with open('src/io/bio/stdfiles.npk', 'w') as f:
    f.write(content)

# 5. src/io/bio/fio.npk: fflush
fflush_code = """    if (fp == 0i64) {
        int64:curr = g_open_files;
        int64:ret = 0i64;
        while (curr != 0i64) {
            FILE->:c = @cast_unchecked<FILE->>(curr);
            if (fflush(curr) == FILE_EOF) {
                ret = FILE_EOF;
            }
            curr = c->next_global;
        }
        pass ret;
    }"""
with open('src/io/bio/fio.npk', 'r') as f:
    content = f.read()
content = content.replace('    if (fp == 0i64) {\n        pass 0i64;\n    }', fflush_code)
with open('src/io/bio/fio.npk', 'w') as f:
    f.write(content)

# 6. src/proc/signal.npk: proc_sigreturn_setup
sigreturn_code = """pub int64:g_sigreturn_tramp = 0i64;

pub func:proc_sigreturn_setup = int64() {
    if (g_sigreturn_tramp != 0i64) {
        pass g_sigreturn_tramp;
    }
    Result<int64>:r = libn_mmap(0i64, 4096i64, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1i64, 0i64);
    if (r.is_error) { pass 0i64; }
    int64:page_addr = r.value;
    uint8->:page = @cast_unchecked<uint8->>(page_addr);
    page[0] = 0x48u8; page[1] = 0xc7u8; page[2] = 0xc0u8; page[3] = 0x0fu8;
    page[4] = 0x00u8; page[5] = 0x00u8; page[6] = 0x00u8; page[7] = 0x0fu8; page[8] = 0x05u8;
    g_sigreturn_tramp = page_addr;
    pass page_addr;
};"""
with open('src/proc/signal.npk', 'r') as f:
    content = f.read()
content = content.replace('pub func:proc_sigreturn_tramp = NIL() {\n    drop(asm!!!<int64>("x86_64", "movq $15, %rax\\n\\tsyscall", ""));\n    pass NIL;\n};', sigreturn_code)
content = content.replace('p[2] = @cast_unchecked<int64>(@proc_sigreturn_tramp);', 'p[2] = proc_sigreturn_setup();')
with open('src/proc/signal.npk', 'w') as f:
    f.write(content)

# 7. src/proc/env.npk: _env_grow caching
env_grow_code = """func:_env_grow = bool() {
    if (_env_heap_count < _env_heap_cap) { pass true; }
    int64:new_cap = _env_heap_cap * 2i64;
    if (new_cap < ENV_INITIAL_CAP) { new_cap = ENV_INITIAL_CAP; }
    Result<int64>:r = mem_realloc(_env_heap_envp, (new_cap + 1i64) * 8i64);
    if (r.is_error) { pass false; }
    int64:new_envp = r.value;

    Result<int64>:r2 = mem_realloc(_env_heap_is_alloc, (new_cap + 1i64) * 8i64);
    if (r2.is_error) { pass false; }
    
    _env_heap_envp = new_envp;
    environ = _env_heap_envp;
    _env_heap_is_alloc = r2.value;
    _env_heap_cap  = new_cap;
    pass true;
};"""
with open('src/proc/env.npk', 'r') as f:
    content = f.read()
content = re.sub(r'func:_env_grow = bool\(\) \{.*?\n\};\n', env_grow_code + '\n', content, flags=re.DOTALL)
with open('src/proc/env.npk', 'w') as f:
    f.write(content)

