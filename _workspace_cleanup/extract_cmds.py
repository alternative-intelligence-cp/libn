import json

transcript_path = "/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/logs/transcript.jsonl"
with open(transcript_path, "r") as f:
    for i, line in enumerate(f):
        try:
            entry = json.loads(line)
            tool_calls = entry.get("tool_calls", [])
            for call in tool_calls:
                if call.get("name") == "default_api:run_command":
                    args = call.get("arguments", {})
                    cmd = args.get("CommandLine", "")
                    print(f"--- Command {i} ---")
                    print(cmd[:100] + ("..." if len(cmd) > 100 else ""))
        except:
            pass
