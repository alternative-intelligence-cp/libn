import json

with open('/home/randy/.gemini/antigravity/brain/bb7ec1eb-281a-4a7b-9faa-24469fae00c8/scratch/all_chunks.json', 'r') as fp:
    chunks = json.load(fp)

for f, reps in chunks.items():
    if "exit.npk" in f:
        for r in reps:
            print("TARGET:", r["TargetContent"])
            print("REPLACE:", r["ReplacementContent"])
