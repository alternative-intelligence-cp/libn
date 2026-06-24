with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

# mremap takes `new_address` as argument 5.
text = text.replace("libn_mremap(@cast_unchecked<any->>(addr), old_length, new_length, flags, 0i64)", "libn_mremap(@cast_unchecked<any->>(addr), old_length, new_length, flags, NULL)")
text = text.replace("libn_mremap(@cast_unchecked<any->>(ptr), old_size, new_size, MREMAP_MAYMOVE, 0i64)", "libn_mremap(@cast_unchecked<any->>(ptr), old_size, new_size, MREMAP_MAYMOVE, NULL)")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)

