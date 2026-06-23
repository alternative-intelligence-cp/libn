with open('src/syscall/syscall.npk', 'r') as f:
    lines = f.readlines()

for idx in [74, 85, 274, 411, 609]:
    print(f"Line {idx+1}: {lines[idx].strip()}")
