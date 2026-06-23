import json

with open('/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/logs/transcript.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'TOOL_CALL':
                for call in data.get('tool_calls', []):
                    args = call.get('args', {})
                    if args.get('TargetFile', '').endswith('file.npk'):
                        print("FOUND MODIFICATION TO file.npk!")
                        print(json.dumps(args, indent=2))
        except:
            pass
