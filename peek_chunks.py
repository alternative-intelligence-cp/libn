import json
with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

lines = chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk']
for i, line in enumerate(lines[150:170]):
    print(f"{150+i+1}: {line}")
