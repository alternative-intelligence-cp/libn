import os

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.npk'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            content = content.replace("*byte", "byte->")
            content = content.replace("*int64", "int64->")
            content = content.replace("*int32", "int32->")
            content = content.replace("*int16", "int16->")
            content = content.replace("*int8", "int8->")
            
            with open(filepath, 'w') as f:
                f.write(content)
