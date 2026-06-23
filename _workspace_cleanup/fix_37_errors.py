import re
import os

def rewrite(filepath, callback):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = callback(content)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

def fix_memutil(c):
    # line 174
    c = c.replace('(@cast_unchecked<int64>(@cast_unchecked<int64>(pa[i]) ^ pb[i]))', '(@cast_unchecked<int64>(pa[i] ^ pb[i]))')
    # line 196
    c = c.replace('raw(replicate_byte(c))', 'raw(replicate_uint8(c))')
    # line 215-216
    c = c.replace('// Match is somewhere in this word — find exact uint8 int64:word_base = ptr + i + wi * 8i64;', '// Match is somewhere in this word — find exact uint8\n            int64:word_base = ptr + i + wi * 8i64;')
    return c
rewrite('src/mem/memutil.npk', fix_memutil)

def fix_slab(c):
    c = c.replace('pub func:slab_alloc = int64(int64:n)', 'pub func:slab_alloc = Result<int64>(int64:n)')
    c = c.replace('pub func:slab_alloc_zero = int64(int64:n)', 'pub func:slab_alloc_zero = Result<int64>(int64:n)')
    c = c.replace('Result<int64>:r = mem_malloc(c.size * count);', 'int64:r_val = raw(mem_malloc(c.size * count));')
    c = c.replace('Result<int64>:r = mem_malloc(c.size);', 'int64:r_val = raw(mem_malloc(c.size));')
    # Need to handle the lines after r_val = ...
    # if (r.is_error) { fail r.error; } pass r.value;  -->  these will be syntax errors now.
    # Instead, let's just make mem_malloc return Result<int64>.
    return c
# rewrite('src/mem/slab.npk', fix_slab)

# Actually, let's make slab_alloc, slab_alloc_zero, and mem_malloc return Result<int64>
def fix_mmap(c):
    c = c.replace('pub func:mem_malloc = int64(int64:size)', 'pub func:mem_malloc = Result<int64>(int64:size)')
    return c
rewrite('src/mem/mmap.npk', fix_mmap)

def fix_slab2(c):
    c = c.replace('pub func:slab_alloc = int64(int64:n)', 'pub func:slab_alloc = Result<int64>(int64:n)')
    c = c.replace('pub func:slab_alloc_zero = int64(int64:n)', 'pub func:slab_alloc_zero = Result<int64>(int64:n)')
    # Result<int64>:r = mem_malloc(c.size); is correct if mem_malloc returns Result<int64>
    return c
rewrite('src/mem/slab.npk', fix_slab2)

def fix_strconv(c):
    # Line 285: Cannot assign value of type 'Result<int64>' to variable of type 'int64'
    # int64:e = libn_errno_set(0i64); -> libn_errno_set returns Result<int64>? No, libn_errno_set is NIL. Wait.
    c = c.replace('int64:e = libn_errno_set', 'drop(libn_errno_set')
    # Also change it for line 309, 337
    c = c.replace('int64:e2 = libn_errno_set', 'drop(libn_errno_set')
    return c
rewrite('src/str/strconv.npk', fix_strconv)

def fix_strlen(c):
    # Line 62: Bitwise operators require same integer type on both sides. Got 'int64' and 'bool'
    # if (s == 0i64 || !has_zero_uint8(s)) -> has_zero_uint8 returns bool.
    # wait... 'has_zero_uint8' returns bool? Let's fix this in strlen.npk
    c = c.replace('has_zero_byte', 'has_zero_uint8')
    c = c.replace('!raw has_zero_uint8', '!(raw has_zero_uint8')
    c = c.replace('pw[wi]))', 'pw[wi])))')
    return c
rewrite('src/str/strlen.npk', fix_strlen)

def fix_tmpfile(c):
    # Line 268: @cast_unchecked<int64>(mode_w_plus_b) -> @cast_unchecked<int64>(@"w+b")
    c = c.replace('@cast_unchecked<int64>(mode_w_plus_b)', '@cast_unchecked<int64>(@"w+b")')
    return c
rewrite('src/io/bio/tmpfile.npk', fix_tmpfile)

def fix_fopen(c):
    # Line 268: FILE->:f = @cast_unchecked<FILE->>(fp);
    c = c.replace('@cast_unchecked<FILE->>(fp)', '@cast_unchecked<FILE->>(fd)')
    c = c.replace('int64:fp = fdopen', 'int64:fd = fdopen')
    return c
rewrite('src/io/bio/fopen.npk', fix_fopen)

def fix_printf(c):
    # Line 226: Unused result from NIL-returning function.
    # drop(fputs(msg, stderr_fp)); -> already drop?
    c = c.replace('bio_ensure_std_init()', 'drop(bio_ensure_std_init())')
    return c
rewrite('src/io/printf.npk', fix_printf)

def fix_file(c):
    c = c.replace('has_zero_byte', 'has_zero_uint8')
    return c
rewrite('src/io/bio/file.npk', fix_file)

def fix_strerror_cast(c):
    c = c.replace('str_int64_to_dec(', 'raw(str_int64_to_dec(')
    return c
rewrite('src/io/bio/strerror.npk', fix_strerror_cast)

def fix_strcpy(c):
    c = c.replace('has_zero_byte', 'has_zero_uint8')
    return c
rewrite('src/str/strcpy.npk', fix_strcpy)
