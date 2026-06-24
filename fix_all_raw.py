import os
import re

# Read errors
with open('clean_errors.txt', 'r') as f:
    errors = f.read().splitlines()

# Load all files
files_cache = {}
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                files_cache[path] = f.read().splitlines()

fixed_count = 0

for err in errors:
    m = re.search(r'Line (\d+),.*into \'([^\']+)\' of type', err)
    if not m:
        continue
    line_no = int(m.group(1))
    var_name = m.group(2)
    
    # Find the file
    matched_file = None
    for path, lines in files_cache.items():
        if len(lines) >= line_no:
            line_content = lines[line_no - 1]
            if var_name in line_content and ('=' in line_content):
                matched_file = path
                break
    
    if matched_file:
        lines = files_cache[matched_file]
        line = lines[line_no - 1]
        
        # Only replace the FIRST '=' that comes after the variable name
        # A simple string replace for the specific variable assignment
        
        # Example line: int64:total = page_align_up(ALLOC_HEADER_SIZE + n);
        # We want: int64:total = raw page_align_up(ALLOC_HEADER_SIZE + n);
        
        if 'raw ' not in line:
            # Find var_name and =
            idx_var = line.find(var_name)
            idx_eq = line.find('=', idx_var)
            if idx_eq != -1:
                # insert 'raw ' after the '='
                # maybe there's a space after '='
                if line[idx_eq+1] == ' ':
                    lines[line_no - 1] = line[:idx_eq+2] + 'raw ' + line[idx_eq+2:]
                else:
                    lines[line_no - 1] = line[:idx_eq+1] + ' raw ' + line[idx_eq+1:]
                fixed_count += 1
                print(f"Fixed {matched_file}:{line_no} ({var_name})")

# Write back
for path, lines in files_cache.items():
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')

print(f"Fixed {fixed_count} errors.")
