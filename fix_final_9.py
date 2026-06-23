with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    # Fix the `end` keyword collision
    lines[i] = lines[i].replace('int64:end,', 'int64:end_idx,')
    lines[i] = lines[i].replace('(end <', '(end_idx <')
    lines[i] = lines[i].replace('> end)', '> end_idx)')
    lines[i] = lines[i].replace(' end;', ' end_idx;')
    lines[i] = lines[i].replace(' end)', ' end_idx)')
    lines[i] = lines[i].replace('= end;', '= end_idx;')
    lines[i] = lines[i].replace(' end -', ' end_idx -')
    
    # Fix the typo ')' ? instead of ':'
    if '*StrView) ? lo =' in lines[i]:
        lines[i] = lines[i].replace('*StrView) ? lo =', '*StrView:lo =')
    if 'stack uint8[64]) ? tmp;' in lines[i]:
        lines[i] = lines[i].replace('stack uint8[64]) ? tmp;', 'stack uint8[64]:tmp;')
    
    # Fix weird @cast_unchecked inside comments that the unfuck script accidentally did
    if '@cast_unchecked' in lines[i] and '//' in lines[i]:
        # we can just strip the weird @cast_unchecked from comments
        import re
        lines[i] = re.sub(r'@cast_unchecked<[^>]+>\(([^)]+)\)', r'\1', lines[i])

with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)
