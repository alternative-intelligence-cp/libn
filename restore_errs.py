import json

with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

print(type(chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk']))
print(type(chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk'][0]))
print(chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk'][0].keys() if isinstance(chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk'][0], dict) else chunks['/home/randy/Workspace/REPOS/libn/src/math/math.npk'][:100])
