import json
with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

c = '\n'.join(chunks['/home/randy/Workspace/REPOS/libn/src/proc/exit.npk'])
for i, line in enumerate(c.split('\n')[70:90]):
    print(f"{70+i+1}: {line}")
