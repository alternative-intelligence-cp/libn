import os

def fix_signal():
    path = '/home/randy/Workspace/REPOS/libn/src/proc/signal.npk'
    with open(path, 'r') as f:
        content = f.read()

    # int64:old_ptr = is old_buf != 0i64 : @old_act[0] => int64 : 0i64;
    content = content.replace('is old_buf != 0i64 : @old_act[0] => int64 : 0i64', '(old_buf != 0i64) ? @cast_unchecked<int64>(@old_act[0]) : 0i64')
    
    # int64:old_p = is old_ptr != 0i64 : @old_val : 0i64;
    content = content.replace('is old_ptr != 0i64 : @old_val : 0i64', '(old_ptr != 0i64) ? @cast_unchecked<int64>(@old_val) : 0i64')
    # wait, @old_val is a pointer to int64, so it should be @cast_unchecked<int64>(@old_val)
    
    # int64:tid = is pid_r.is_error : 1i64 : pid_r.val;
    # wait, fix_syntax_global already might have run, so let's just do .replace()
    content = content.replace('is pid_r.is_error : 1i64 : pid_r.val', '(pid_r.is_error) ? 1i64 : pid_r.value')
    
    # fix the other .val
    content = content.replace('pid_r.val', 'pid_r.value')
    content = content.replace('err_r.val', 'err_r.value')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_errno():
    path = '/home/randy/Workspace/REPOS/libn/src/syscall/errno.npk'
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace('global int64:g_libn_errno = 0i64;', 'pub int64:g_libn_errno = 0i64;')
    
    # int64:abs_e = is e < 0i64 : 0i64 - e : e;
    content = content.replace('is e < 0i64 : 0i64 - e : e', '(e < 0i64) ? (0i64 - e) : e')
    
    with open(path, 'w') as f:
        f.write(content)

def fix_exit():
    path = '/home/randy/Workspace/REPOS/libn/src/proc/exit.npk'
    with open(path, 'r') as f:
        content = f.read()
    # _?(fn => (NIL)())();
    # Let's replace with:
    # 1. Cast fn to int64 (it already is)
    # Actually wait. In v0.12.x, function pointer type is `(NIL)()`.
    # Let's try to just do: `_?(@cast_unchecked<int64>(fn))();`
    # No, that will be "Cannot call non-function type".
    # Wait, in the C FFI, we cast function pointers to thin pointers.
    # What if we just call the function by cheating the compiler?
    # No, we need a valid type. If `@cast_unchecked<(NIL)()>` didn't parse, what about `NIL()` ?
    # Let's use `@cast_unchecked<func() -> NIL>(fn)` ? No, `func` is a keyword but maybe not a type.
    # Let's look at type parsing again.
    
    # For now let's just do: _?(@cast_unchecked<NIL()>(fn))(); 
    # Wait! If the type parser expects a parenthesis, maybe we need space? `@cast_unchecked< NIL() >(fn)()`
    pass

fix_signal()
fix_errno()
