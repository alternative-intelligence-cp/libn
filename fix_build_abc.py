with open("build.abc", "r") as f:
    lines = f.readlines()

sources = []
in_sources = False
for line in lines:
    if "sources: [" in line and not in_sources:
        in_sources = True
    elif in_sources and "];" in line:
        in_sources = False
        break
    elif in_sources and line.strip().startswith('"'):
        sources.append(line.strip().strip(','))

# Now write the new build.abc
with open("build.abc", "w") as f:
    f.write('[project]\n')
    f.write('name = "libn"\n')
    f.write('version = "0.11.5"\n\n')
    
    f.write('[target.libn]\n')
    f.write('type = "library"\n')
    f.write('sources = [\n')
    for s in sources:
        f.write(f'    {s},\n')
    f.write(']\n')
    f.write('flags = ["-O3", "--verify", "-Wno-unused-variable"]\n')

print("Fixed build.abc")
