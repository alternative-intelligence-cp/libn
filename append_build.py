import re

with open("build_errors.txt", "r") as f:
    text = f.read()

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_text = ansi_escape.sub('', text)

with open("/home/randy/Workspace/META/LIBN/audits/a30/compilation.md", "a") as f:
    f.write("\n\n================================================================================\n")
    f.write("BUILD OUTPUT\n")
    f.write("================================================================================\n\n")
    f.write("```\n")
    f.write(clean_text)
    f.write("\n```\n")
