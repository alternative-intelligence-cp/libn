import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Revert Result<int64> in function signatures
    content = re.sub(r'pub func:([a-zA-Z0-9_]+) = Result<int64>\(', r'pub func:\1 = int64(', content)
    content = re.sub(r'func:([a-zA-Z0-9_]+) = Result<int64>\(', r'func:\1 = int64(', content)

    # Note: void or NIL? Originally it was void(). Wait, in libn_exit_group it was void.
    # What about libn_fork? It was Result<int64>().
    
    with open(filepath, "w") as f:
        f.write(content)

fix_file("src/syscall/syscall.npk")
fix_file("src/mem/slab.npk")
