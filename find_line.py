import sys

def find_line():
    with open('src/all.npk', 'r') as f:
        lines = f.readlines()
        
    files = []
    for line in lines:
        if 'use ' in line:
            parts = line.split('"')
            if len(parts) >= 3:
                files.append('src/' + parts[1])
                
    total_lines = 0
    for file in files:
        with open(file, 'r') as f:
            flines = f.readlines()
            for local_line_num, content in enumerate(flines, 1):
                total_lines += 1
                if total_lines == 108:
                    print(f"Global line 108 is local line {local_line_num} of {file}:")
                    print(content.rstrip())
                    return

find_line()
