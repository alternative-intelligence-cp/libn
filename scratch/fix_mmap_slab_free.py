with open('src/mem/mmap.npk', 'r') as f:
    text = f.read()

text = text.replace("extern func:libn_slab_free = int64(int64:ptr);", "extern func:libn_slab_free = int64(any->:ptr);")
text = text.replace("drop(libn_slab_free(ptr));", "drop(libn_slab_free(@cast_unchecked<any->>(ptr)));")

with open('src/mem/mmap.npk', 'w') as f:
    f.write(text)
