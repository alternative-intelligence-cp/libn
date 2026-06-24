import os

files = ["src/mem/mmap.npk", "src/mem/memcpy.npk", "src/mem/memset.npk", "src/mem/slab.npk"]
decl = "extern func:failsafe = int32(tbb32:err);\n"

for fpath in files:
    with open(fpath, "r") as f:
        content = f.read()
    if decl not in content:
        # Insert after the last use statement, or at the top
        lines = content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("use "):
                insert_idx = i + 1
        
        lines.insert(insert_idx, decl)
        with open(fpath, "w") as f:
            f.write("\n".join(lines) + "\n")

