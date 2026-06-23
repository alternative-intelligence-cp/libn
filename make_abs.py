import os
import glob

files = glob.glob("src/**/*.npk", recursive=True)
for f in files:
    with open(f, "r") as file:
        content = file.read()
    content = content.replace('use "src/', 'use "/home/randy/Workspace/REPOS/libn/src/')
    with open(f, "w") as file:
        file.write(content)
