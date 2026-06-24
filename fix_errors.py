import os

fixes = {
    "src/str/strlen.npk": [
        ("pass n;", "pass Result<int64>(n);"), # Wait, does pass n work? Let's check.
    ]
}
