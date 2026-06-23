import re
with open("src/io/bio/fopen.npk", "r") as f:
    content = f.read()

content = re.sub(r'^\}$', '};', content, flags=re.MULTILINE)

# But wait, this will replace ALL '}'.
# Actually, Nitpick requires `};` for functions, structs, traits.
# So `^}$` might be `if` blocks. Wait, `if` blocks shouldn't start at column 0!
# If the code is properly indented, `if` blocks end with `    }` (4 spaces).
# So `^}$` without leading spaces ONLY matches top-level constructs!
