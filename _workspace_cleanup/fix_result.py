import os

def fix_result(path):
    with open(path, 'r') as f:
        code = f.read()

    orig_code = code

    # Replace Result<int64> with int64
    code = code.replace('Result<int64>', 'int64')

    if code != orig_code:
        with open(path, 'w') as f:
            f.write(code)
        print(f"Fixed Result in {path}")

def main():
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                fix_result(os.path.join(root, file))

if __name__ == "__main__":
    main()
