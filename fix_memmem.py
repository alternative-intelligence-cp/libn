with open('src/mem/memutil.npk', 'r') as f:
    content = f.read()

target = """    if (nlen == 1i64) {
        pass mem_memchr(haystack, @cast_unchecked<int64>(n[0]), hlen);
    }

      // Boyer-Moore-Horspool algorithm"""

replacement = """    if (nlen == 1i64) {
        pass mem_memchr(haystack, @cast_unchecked<int64>(n[0]), hlen);
    }

      // Fast-path naive search for small needles (avoids 2KB stack init overhead)
    if (nlen <= 8i64) {
        int64:last = hlen - nlen;
        int64:hi = 0i64;
        while (hi <= last) {
            bool:match = true;
            int64:ni = 0i64;
            while (ni < nlen) {
                if (h[hi + ni] != n[ni]) {
                    match = false;
                    break;
                }
                ni = ni + 1i64;
            }
            if (match) {
                pass haystack + hi;
            }
            hi = hi + 1i64;
        }
        pass 0i64;
    }

      // Boyer-Moore-Horspool algorithm"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/mem/memutil.npk', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Target not found.")
