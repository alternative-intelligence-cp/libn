import re

# io/bio/strerror.npk
file = "src/io/bio/strerror.npk"
with open(file, "r") as f: text = f.read()
text = re.sub(r'\{ ([0-9-]+)i64,\s+"([^"]+)" as int64 \}', r'{ \1i64, @cast_unchecked<int64>(@"\2"[0]) }', text)
with open(file, "w") as f: f.write(text)

# proc/exec.npk
file = "src/proc/exec.npk"
with open(file, "r") as f: text = f.read()
text = text.replace('"PATH" as int64', '@cast_unchecked<int64>(@"PATH"[0])')
text = text.replace('"/usr/local/bin:/usr/bin:/bin" as int64', '@cast_unchecked<int64>(@"/usr/local/bin:/usr/bin:/bin"[0])')
with open(file, "w") as f: f.write(text)

# str/strview.npk
file = "src/str/strview.npk"
with open(file, "r") as f: text = f.read()
text = text.replace('pass ((@cast_unchecked<*byte[]>(s.ptr))[s.len - 1i64]) as int64;', 'pass @cast_unchecked<int64>((@cast_unchecked<*byte[]>(s.ptr))[s.len - 1i64]);')
with open(file, "w") as f: f.write(text)
