import os
import subprocess

target_dir = "/home/randy/Workspace/META/LIBN/audits/a34"
os.makedirs(target_dir, exist_ok=True)

with open(f"{target_dir}/compilation.md", "w") as out:
    for root, _, files in os.walk("src"):
        for file in sorted(files):
            if file.endswith(".npk"):
                path = os.path.join(root, file)
                out.write(f"\n\n# FILE: {path}\n")
                with open(path, "r") as f:
                    out.write(f.read())

    out.write("\n\n# BUILD OUTPUT\n")
    # Actually run the compiler to get the exact output
    result = subprocess.run(["npkc", "-c", "src/all.npk"], capture_output=True, text=True)
    out.write(result.stdout)
    out.write(result.stderr)

print("Compilation file generated for A34.")
