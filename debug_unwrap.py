import re

line_str = "    int64:head = slab_freelist_get(cls);\n"
new_line = re.sub(r'(=\s*|pass\s+|if\s*\(?|while\s*\(?|return\s+)([a-zA-Z_]\w*\s*\()', r'\1raw \2', line_str, count=1)
print(repr(new_line))

