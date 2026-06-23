import subprocess

def fix_file(path, replacements):
    with open(path, "r") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)

fix_file("src/io/bio/fchar.npk", [
    ("if (f->flags & FILE_FLAG_WRITE_MODE) != 0i64) {", "if ((f->flags & FILE_FLAG_WRITE_MODE) != 0i64) {")
])

fix_file("src/io/bio/fseek.npk", [
    ("if (f->flags & FILE_FLAG_WRITE_MODE) != 0i64 && f.buf_pos > 0i64) {", "if ((f->flags & FILE_FLAG_WRITE_MODE) != 0i64 && f.buf_pos > 0i64) {")
])

fix_file("src/str/strview.npk", [
    ("if (!(len < 0i64) {", "if (!(len < 0i64)) {"),
    ("if (!(sa.len < sb->len) {", "if (!(sa.len < sb->len)) {"),
    ("if (strview_starts_with(sv, prefix) {", "if (strview_starts_with(sv, prefix)) {"),
    ("if (strview_starts_with_str(sv, prefix) {", "if (strview_starts_with_str(sv, prefix)) {"),
    ("if (!(prefix != 0i64) {", "if (!(prefix != 0i64)) {"),
    ("if (strview_ends_with(sv, suffix) {", "if (strview_ends_with(sv, suffix)) {"),
    ("if (strview_ends_with_str(sv, suffix) {", "if (strview_ends_with_str(sv, suffix)) {"),
    ("if (!(suffix != 0i64) {", "if (!(suffix != 0i64)) {"),
    ("if (!(s->len < buflen) {", "if (!(s->len < buflen)) {"),
    ("if (!(s->len < max) {", "if (!(s->len < max)) {"),
    ("pass ((@cast_unchecked<uint8->>(s->ptr))[i]) as int64;", "pass @cast_unchecked<int64>((@cast_unchecked<uint8->>(s->ptr))[i]);"),
    ("pass ((@cast_unchecked<uint8->>(s->ptr))[s->len - 1i64]) as int64;", "pass @cast_unchecked<int64>((@cast_unchecked<uint8->>(s->ptr))[s->len - 1i64]);")
])

print("Fixed final files")
