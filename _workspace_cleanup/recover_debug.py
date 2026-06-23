import json

transcript_path = "/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/logs/transcript.jsonl"
with open(transcript_path, "r") as f:
    for line in f:
        try:
            entry = json.loads(line)
        except:
            continue
            
        if entry.get("source") != "MODEL":
            continue
            
        tool_calls = entry.get("tool_calls", [])
        for call in tool_calls:
            name = call.get("name", "")
            if "replace_file_content" in name:
                args = call.get("arguments", {})
                target = args.get("TargetFile")
                print(f"Tool: {name}, Target: {target}")
