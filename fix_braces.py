import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # In Nitpick, `};` is for struct and func declarations.
    # We should ensure `if` and `while` do NOT have `};`.
    # Actually, simply `};` where it's not a struct or func is illegal.
    
    # We will do a robust matching of functions to add `};` if missing,
    # and remove stray `;` after `}` if it's an `if`/`while` block.
    # Since it's easier, let's just replace `\n            };` with `\n            }` in syscall.npk
    
    if "syscall.npk" in path:
        content = content.replace("            };\n", "            }\n")

    if "math.npk" in path:
        # Revert the dumb regex
        content = content.replace("};\n", "}\n")
        content = content.replace("}; \n", "} \n")
        
        # Now add `};` properly to functions
        lines = content.split('\n')
        in_func = False
        depth = 0
        for i, line in enumerate(lines):
            if line.startswith('pub func:') or line.startswith('func:'):
                in_func = True
                depth = 0
            
            if in_func:
                depth += line.count('{') - line.count('}')
                if depth == 0 and '}' in line:
                    lines[i] = line.replace('}', '};')
                    in_func = False
        content = '\n'.join(lines)

    with open(path, 'w') as f:
        f.write(content)

fix_file('/home/randy/Workspace/REPOS/libn/src/math/math.npk')
fix_file('/home/randy/Workspace/REPOS/libn/src/syscall/syscall.npk')
