with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

text = text.replace("libn_mremap(@cast_unchecked<any->>(old_addr), old_size, new_size, flags, new_addr)", "libn_mremap(@cast_unchecked<any->>(old_addr), old_size, new_size, flags, @cast_unchecked<any->>(new_addr))")
text = text.replace("libn_mremap(@cast_unchecked<any->>(map_start), old_map_size, new_total, MREMAP_MAYMOVE, 0i64)", "libn_mremap(@cast_unchecked<any->>(map_start), old_map_size, new_total, MREMAP_MAYMOVE, NULL)")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
