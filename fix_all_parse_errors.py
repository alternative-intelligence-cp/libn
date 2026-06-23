def replace(path, old, new):
    with open(path, 'r') as f:
        s = f.read()
    s = s.replace(old, new)
    with open(path, 'w') as f:
        f.write(s)

replace('src/mem/mmap.npk', 'if (size > 0i64 && n > (9223372036854775807i64 / size) {', 'if (size > 0i64 && n > (9223372036854775807i64 / size)) {')
replace('src/io/bio/file.npk', 'if (total_read < n && (f->flags & FIO_EOF) == 0i64 {', 'if (total_read < n && (f->flags & FIO_EOF) == 0i64) {')
replace('src/io/bio/file.npk', 'if (total_written < n && (f->flags & FIO_ERR) == 0i64 {', 'if (total_written < n && (f->flags & FIO_ERR) == 0i64) {')
replace('src/str/strfmt.npk', 'if (ch == 37i8 {', 'if (ch == 37i8) {')
replace('src/str/strfmt.npk', 'if (num == 0i64 {', 'if (num == 0i64) {')
replace('src/str/strfmt.npk', 'if (n < 0i64 {', 'if (n < 0i64) {')
replace('src/math/math.npk', 'if (x < 0i64 {', 'if (x < 0i64) {')
replace('src/math/math.npk', 'if (y < 0i64 {', 'if (y < 0i64) {')
replace('src/math/math.npk', 'if (val < 0i64 {', 'if (val < 0i64) {')
replace('src/math/math.npk', 'if (num < 0i64 {', 'if (num < 0i64) {')
replace('src/mem/memutil.npk', 'if (ptr == 0i64 {', 'if (ptr == 0i64) {')
replace('src/mem/slab.npk', 'if (n > SLAB_THRESHOLD {', 'if (n > SLAB_THRESHOLD) {')
replace('src/str/strlen.npk', 'while (n > 0i64 {', 'while (n > 0i64) {')
replace('src/str/strlen.npk', 'while (n > 0i64 && (b != 0i8) {', 'while (n > 0i64 && b != 0i8) {')
