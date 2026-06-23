import os, re

def process(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    new_content = content.replace("=> pass ", "=> ")

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".npk"):
            process(os.path.join(root, file))
