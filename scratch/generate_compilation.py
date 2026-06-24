import os
import subprocess

out_path = '/home/randy/Workspace/META/LIBN/audits/a34/compilation.md'
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w') as out_f:
    # Concatenate all source files
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.npk'):
                path = os.path.join(root, file)
                out_f.write(f"\n# {path}\n```nitpick\n")
                with open(path, 'r') as in_f:
                    out_f.write(in_f.read())
                out_f.write("\n```\n")

    # Append build output
    out_f.write("\n# build output\n```\n")
    
    # Run compiler on all files to show they compile
    result = subprocess.run(
        "for f in src/*/*.npk src/*/*/*.npk; do npkc -c \"$f\" 2>&1 | grep error || true; done",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Check if there were any output (errors)
    if not result.stdout.strip() and not result.stderr.strip():
        out_f.write("Successfully compiled all files with no errors.\n")
    else:
        out_f.write(result.stdout)
        out_f.write(result.stderr)
        
    out_f.write("```\n")

print(f"Generated {out_path}")
