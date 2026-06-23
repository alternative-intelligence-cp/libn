import os
import re

src_dir = "/home/randy/Workspace/REPOS/libn/src"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".npk"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()

            new_content = content
            
            # Replace f. with f-> for FILE->:f
            # Be careful not to replace f.e.g. `f.e.` or something.
            # Only match known fields:
            fields = ['fd', 'flags', 'buf_pos', 'buf_len', 'buf_cap', 'buf', 'file_pos', 'unget', 'buf_mode', 'next_global']
            for field in fields:
                new_content = re.sub(r'\bf\.' + field + r'\b', 'f->' + field, new_content)
                new_content = re.sub(r'\bcurr_f\.' + field + r'\b', 'curr_f->' + field, new_content)
                new_content = re.sub(r'\bsin\.' + field + r'\b', 'sin->' + field, new_content)
                new_content = re.sub(r'\bsout\.' + field + r'\b', 'sout->' + field, new_content)
                new_content = re.sub(r'\bserr\.' + field + r'\b', 'serr->' + field, new_content)
            
            # For StrView->:s, n, sa, sb
            sv_fields = ['ptr', 'len']
            for var in ['s', 'n', 'sa', 'sb', 'view']:
                for field in sv_fields:
                    new_content = re.sub(r'\b' + var + r'\.' + field + r'\b', var + '->' + field, new_content)

            # For StrBuf->:sb
            sb_fields = ['ptr', 'len', 'cap']
            for field in sb_fields:
                new_content = re.sub(r'\bsb\.' + field + r'\b', 'sb->' + field, new_content)

            # For StrFmtState->:st
            st_fields = ['buf', 'capacity', 'length', 'error']
            for field in st_fields:
                new_content = re.sub(r'\bst\.' + field + r'\b', 'st->' + field, new_content)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Fixed {path}")

