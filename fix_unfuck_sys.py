import re
import glob

for file in glob.glob('src/**/*.npk', recursive=True):
    with open(file, 'r') as fp:
        c = fp.read()
    
    def clean(m):
        args = m.group(1)
        block = m.group(0).strip()
        last_line = block.split('\n')[-1]
        
        m2 = re.search(r'(?:int64:|int32:)?([a-zA-Z0-9_]+)\s*=\s*(?:@cast_unchecked<int32>\()?res_', last_line)
        if not m2:
            return m.group(0) # fail safe
        
        var = m2.group(1)
        is_decl = "int64:" in last_line or "int32:" in last_line
        is_int32 = "int32:" in last_line
        
        res = f"Result<int64>:res_{var} = sys({args});\n"
        res += f"    if (res_{var}.is_error) {{ fail @cast_unchecked<tbb8>(res_{var}.error); }}\n"
        if is_decl:
            if is_int32:
                res += f"    int32:{var} = @cast_unchecked<int32>(res_{var}.value);"
            else:
                res += f"    int64:{var} = res_{var}.value;"
        else:
            res += f"    {var} = res_{var}.value;"
        return res
        
    # Match the sys call and all subsequent lines that are part of the unwrapping garbage
    # The garbage lines contain `.is_error` or `= res_`
    c = re.sub(r'Result<int64>:.*?=\s*sys\((.*?)\);\n(?:\s*if\s*\(.*?\.is_error.*?\n|\s*(?:int64:|int32:)?.*?=\s*(?:@cast_unchecked<int32>\()?res_.*?.value.*?\n?)+', clean, c)
    
    with open(file, 'w') as fp:
        fp.write(c)

print("Unfucked sys calls.")
