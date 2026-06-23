with open('src/str/strview.npk', 'r') as f:
    lines = f.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].replace('left.ptr', 'left->ptr')
    lines[i] = lines[i].replace('left.len', 'left->len')
    lines[i] = lines[i].replace('right.ptr', 'right->ptr')
    lines[i] = lines[i].replace('right.len', 'right->len')
    lines[i] = lines[i].replace('tmp.ptr', 'tmp->ptr')
    lines[i] = lines[i].replace('tmp.len', 'tmp->len')
    lines[i] = lines[i].replace('tmp[s', 'tmp[s') # Wait, tmp is an array in one place?
    lines[i] = lines[i].replace('bv.ptr', 'bv->ptr')
    lines[i] = lines[i].replace('bv.len', 'bv->len')

with open('src/str/strview.npk', 'w') as f:
    f.writelines(lines)
