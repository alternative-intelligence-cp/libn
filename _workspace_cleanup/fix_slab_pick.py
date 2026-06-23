with open("src/mem/slab.npk", "r") as f:
    content = f.read()

content = content.replace('''    pick i {
        0i64 => pass 8i64;
        1i64 => pass 16i64;
        2i64 => pass 32i64;
        3i64 => pass 64i64;
        4i64 => pass 128i64;
        5i64 => pass 256i64;
        6i64 => pass 512i64;
        7i64 => pass 1024i64;
        8i64 => pass 2048i64;
        _    => pass 0i64;
    }''', '''    if i == 0i64 { pass 8i64; }
    else if i == 1i64 { pass 16i64; }
    else if i == 2i64 { pass 32i64; }
    else if i == 3i64 { pass 64i64; }
    else if i == 4i64 { pass 128i64; }
    else if i == 5i64 { pass 256i64; }
    else if i == 6i64 { pass 512i64; }
    else if i == 7i64 { pass 1024i64; }
    else if i == 8i64 { pass 2048i64; }
    else { pass 0i64; }''')

content = content.replace('''    pick i {
        0i64 => pass SLAB_SLOTS_PER_PAGE_0;
        1i64 => pass SLAB_SLOTS_PER_PAGE_1;
        2i64 => pass SLAB_SLOTS_PER_PAGE_2;
        3i64 => pass SLAB_SLOTS_PER_PAGE_3;
        4i64 => pass SLAB_SLOTS_PER_PAGE_4;
        5i64 => pass SLAB_SLOTS_PER_PAGE_5;
        6i64 => pass SLAB_SLOTS_PER_PAGE_6;
        7i64 => pass SLAB_SLOTS_PER_PAGE_7;
        8i64 => pass SLAB_SLOTS_PER_PAGE_8;
        _    => pass 0i64;
    }''', '''    if i == 0i64 { pass SLAB_SLOTS_PER_PAGE_0; }
    else if i == 1i64 { pass SLAB_SLOTS_PER_PAGE_1; }
    else if i == 2i64 { pass SLAB_SLOTS_PER_PAGE_2; }
    else if i == 3i64 { pass SLAB_SLOTS_PER_PAGE_3; }
    else if i == 4i64 { pass SLAB_SLOTS_PER_PAGE_4; }
    else if i == 5i64 { pass SLAB_SLOTS_PER_PAGE_5; }
    else if i == 6i64 { pass SLAB_SLOTS_PER_PAGE_6; }
    else if i == 7i64 { pass SLAB_SLOTS_PER_PAGE_7; }
    else if i == 8i64 { pass SLAB_SLOTS_PER_PAGE_8; }
    else { pass 0i64; }''')

content = content.replace('''    pick i {
        0i64 => pass g_slab_freelist_0;
        1i64 => pass g_slab_freelist_1;
        2i64 => pass g_slab_freelist_2;
        3i64 => pass g_slab_freelist_3;
        4i64 => pass g_slab_freelist_4;
        5i64 => pass g_slab_freelist_5;
        6i64 => pass g_slab_freelist_6;
        7i64 => pass g_slab_freelist_7;
        8i64 => pass g_slab_freelist_8;
        _    => pass 0i64;
    }''', '''    if i == 0i64 { pass g_slab_freelist_0; }
    else if i == 1i64 { pass g_slab_freelist_1; }
    else if i == 2i64 { pass g_slab_freelist_2; }
    else if i == 3i64 { pass g_slab_freelist_3; }
    else if i == 4i64 { pass g_slab_freelist_4; }
    else if i == 5i64 { pass g_slab_freelist_5; }
    else if i == 6i64 { pass g_slab_freelist_6; }
    else if i == 7i64 { pass g_slab_freelist_7; }
    else if i == 8i64 { pass g_slab_freelist_8; }
    else { pass 0i64; }''')

content = content.replace('''    pick i {
        0i64 => { g_slab_freelist_0 = val; }
        1i64 => { g_slab_freelist_1 = val; }
        2i64 => { g_slab_freelist_2 = val; }
        3i64 => { g_slab_freelist_3 = val; }
        4i64 => { g_slab_freelist_4 = val; }
        5i64 => { g_slab_freelist_5 = val; }
        6i64 => { g_slab_freelist_6 = val; }
        7i64 => { g_slab_freelist_7 = val; }
        8i64 => { g_slab_freelist_8 = val; }
        _    => {}
    }''', '''    if i == 0i64 { g_slab_freelist_0 = val; }
    else if i == 1i64 { g_slab_freelist_1 = val; }
    else if i == 2i64 { g_slab_freelist_2 = val; }
    else if i == 3i64 { g_slab_freelist_3 = val; }
    else if i == 4i64 { g_slab_freelist_4 = val; }
    else if i == 5i64 { g_slab_freelist_5 = val; }
    else if i == 6i64 { g_slab_freelist_6 = val; }
    else if i == 7i64 { g_slab_freelist_7 = val; }
    else if i == 8i64 { g_slab_freelist_8 = val; }
    else {}''')

with open("src/mem/slab.npk", "w") as f:
    f.write(content)
