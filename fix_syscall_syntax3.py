with open('src/syscall/syscall.npk', 'r') as f:
    s = f.read()

s = s.replace('int64:flags)) {', 'int64:flags) {')
s = s.replace('int64:size)) {', 'int64:size) {')
s = s.replace('int64:ts_req)) {', 'int64:ts_req) {')

s = s.replace('r.@cast_unchecked<int64>(err)', '@cast_unchecked<int64>(r.err)')
s = s.replace('r.err', 'r.error')

with open('src/syscall/syscall.npk', 'w') as f:
    f.write(s)
