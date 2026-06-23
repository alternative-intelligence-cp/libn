import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            def replacer(match):
                call_args = match.group(1)
                num_commas = call_args.count(',')
                if num_commas == 7:
                    return f"str_snprintf5({call_args})"
                elif num_commas == 9:
                    return f"str_snprintf7({call_args})"
                return match.group(0)
            
            new_content = re.sub(r'str_snprintf8\(([^)]+)\)', replacer, content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed snprintf in {path}")

# Now add str_snprintf5 and str_snprintf7 to strfmt.npk
strfmt_path = os.path.join(src_dir, 'str/strfmt.npk')
with open(strfmt_path, 'r') as f:
    strfmt_content = f.read()

if 'str_snprintf5' not in strfmt_content:
    strfmt_content += """
// Five-arg version
pub func:str_snprintf5 = int64(int64:buf, int64:buf_size, int64:fmt,
                                int64:a0, int64:a1, int64:a2,
                                int64:a3, int64:a4) {
    stack int64[5]:a;
    a[0]=a0; a[1]=a1; a[2]=a2; a[3]=a3; a[4]=a4;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 5i64);
};

// Seven-arg version
pub func:str_snprintf7 = int64(int64:buf, int64:buf_size, int64:fmt,
                                int64:a0, int64:a1, int64:a2, int64:a3,
                                int64:a4, int64:a5, int64:a6) {
    stack int64[7]:a;
    a[0]=a0; a[1]=a1; a[2]=a2; a[3]=a3;
    a[4]=a4; a[5]=a5; a[6]=a6;
    pass raw str_format_args(buf, buf_size, fmt, @a[0], 7i64);
};
"""
    with open(strfmt_path, 'w') as f:
        f.write(strfmt_content)
    print("Added str_snprintf5 and str_snprintf7 to strfmt.npk")

print("Done")
