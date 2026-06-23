import re

with open("src/syscall/syscall.npk", "r") as f:
    content = f.read()

# Remove the sys_safe definitions
content = re.sub(r'pub func:sys_safe =.*?pass ret;\n};\n', '', content, flags=re.DOTALL)
content = re.sub(r'pub func:sys[1-5] =.*?\};\n', '', content, flags=re.DOTALL)

# Remove sys_full definitions
content = re.sub(r'pub func:sys_full =.*?pass ret;\n};\n', '', content, flags=re.DOTALL)
content = re.sub(r'pub func:sys_full[1-5] =.*?\};\n', '', content, flags=re.DOTALL)

# Remove sys_raw definition
content = re.sub(r'pub func:sys_raw =.*?pass ret;\n};\n', '', content, flags=re.DOTALL)

with open("src/syscall/syscall.npk", "w") as f:
    f.write(content)
