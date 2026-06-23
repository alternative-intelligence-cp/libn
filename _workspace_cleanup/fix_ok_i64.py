import re
with open("src/io/bio/fprintf.npk", "r") as f:
    content = f.read()

# Remove the dummy declarations
content = re.sub(r'\s*Result<int64>:r_p = ok_i64\(0i64\);', '', content)

# Change assignment to declaration
content = content.replace('r_p = mem_malloc(', 'Result<int64>:r_p = mem_malloc(')

with open("src/io/bio/fprintf.npk", "w") as f:
    f.write(content)
