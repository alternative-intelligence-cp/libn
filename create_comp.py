import os
import re

out_file = "/home/randy/Workspace/META/LIBN/audits/a30/compilation.md"
src_dir = "/home/randy/Workspace/REPOS/libn/src"

with open(out_file, "w") as out:
    for root, dirs, files in os.walk(src_dir):
        for file in sorted(files):
            if file.endswith(".npk"):
                if file == "all.npk":
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, "/home/randy/Workspace/REPOS/libn")
                out.write(f"## {rel_path}\n\n```nitpick\n")
                with open(full_path, "r") as f:
                    content = f.read()
                    out.write(content)
                    if not content.endswith("\n"):
                        out.write("\n")
                out.write("```\n\n")
    
    out.write("## Build Output\n\n```text\n")
    with open("/home/randy/Workspace/REPOS/libn/build_errors.txt", "r") as f:
        text = f.read()
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_text = ansi_escape.sub('', text)
        out.write(clean_text)
    out.write("\n```\n")
