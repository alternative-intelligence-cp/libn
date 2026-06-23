import os, re

def process(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        
    old_content = content

    # 1. fail expr as tbb8; -> fail expr;
    content = re.sub(r'fail\s+([A-Za-z0-9_.()]+)\s+as\s+tbb8\s*;', r'fail \1;', content)
    content = re.sub(r'fail\s+([A-Za-z0-9_.()]+)\s+as\s+tbb32\s*;', r'fail \1;', content)
    content = re.sub(r'fail\s+([A-Za-z0-9_.]+)\s+as\s+tbb8\s*;', r'fail \1;', content)
    content = re.sub(r'fail\s+e\s+as\s+tbb8\s*;', r'fail e;', content)
    content = re.sub(r'fail\s+([A-Za-z0-9_]+)\s+as\s+tbb8\s*;', r'fail \1;', content)

    # 2. *Type:var = expr as *Type; -> Type->:var = @cast_unchecked<Type->>(expr);
    content = re.sub(r'\*([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_.]+)\s+as\s+\*[a-zA-Z0-9_]+\s*;', 
                     r'\1->:\2 = @cast_unchecked<\1->>(\3);', content)
                     
    # 3. (s.ptr as *byte)[0] -> (@cast_unchecked<uint8->>(s.ptr))[0]
    content = re.sub(r'\(([a-zA-Z0-9_.]+)\s+as\s+\*byte\)\s*\[', r'(@cast_unchecked<uint8->>(\1))[', content)
    
    # 4. expr as *Type -> @cast_unchecked<Type->>(expr)
    content = re.sub(r'([a-zA-Z0-9_.()]+)\s+as\s+\*([a-zA-Z0-9_]+)', r'@cast_unchecked<\2->>(\1)', content)

    # Replace 'byte->' with 'uint8->' since byte is pseudo-code
    content = content.replace("byte->", "uint8->")

    # 5. pub struct FILE { -> pub struct:FILE {
    content = re.sub(r'pub\s+struct\s+([a-zA-Z0-9_]+)\s*\{', r'pub struct:\1 {', content)
    content = re.sub(r'^struct\s+([a-zA-Z0-9_]+)\s*\{', r'struct:\1 {', content, flags=re.MULTILINE)

    if content != old_content:
        with open(filepath, "w") as f:
            f.write(content)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process(os.path.join(root, file))
