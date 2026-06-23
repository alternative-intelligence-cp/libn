import os
import re

bio_dir = "/home/randy/Workspace/REPOS/libn/src/io/bio"

def fix_unused_results():
    pattern = re.compile(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^;]*\);')
    ignore_words = {'drop', 'pass', 'fail', 'exit', 'if', 'while', 'for', 'return', 'use', 'int64', 'int32', 'uint8', 'bool', 'Result'}
    
    for root, _, files in os.walk(bio_dir):
        for filename in files:
            if not filename.endswith(".npk"): continue
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            changed = False
            for i in range(len(lines)):
                # Ignore variable declarations like int64:r = func();
                if ":" in lines[i].split("(")[0]: 
                    continue
                # Ignore assignment like r = func();
                if "=" in lines[i].split("(")[0]:
                    continue

                m = pattern.match(lines[i])
                if m:
                    word = m.group(2)
                    if word not in ignore_words:
                        # Don't replace if it's a cast like @cast_unchecked
                        if "@" in lines[i]:
                            continue
                        # Use drop
                        lines[i] = m.group(1) + "drop " + lines[i].lstrip()
                        changed = True
            
            # Special case fixes for mkstemp calls
            for i in range(len(lines)):
                if "int64:fd = mkstemp(" in lines[i]:
                    lines[i] = lines[i].replace("int64:fd = mkstemp(", "int64:fd = raw mkstemp(")
                    changed = True
                if "int64:fp =" in lines[i] and "fdopen(" in lines[i]:
                    lines[i] = lines[i].replace("fdopen(", "raw fdopen(")
                    changed = True
                if "int64:fd =" in lines[i] and "libn_open(" in lines[i]:
                    lines[i] = lines[i].replace("libn_open(", "raw libn_open(")
                    changed = True
                if "int64:r =" in lines[i] and "libn_close(" in lines[i]:
                    lines[i] = lines[i].replace("libn_close(", "raw libn_close(")
                    changed = True
            
            if changed:
                with open(filepath, 'w') as f:
                    f.writelines(lines)
                print(f"Fixed unused results in {filename}")

fix_unused_results()
