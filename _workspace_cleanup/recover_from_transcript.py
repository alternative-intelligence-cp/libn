import json
import os

transcript_path = "/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/logs/transcript.jsonl"
file_contents = {}

with open(transcript_path, "r") as f:
    for line in f:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        if entry.get("type") == "TOOL_CALL" and "tool_calls" in entry:
            for call in entry["tool_calls"]:
                name = call.get("name")
                args = call.get("arguments", {})
                
                if name == "default_api:write_to_file":
                    target = args.get("TargetFile")
                    content = args.get("CodeContent")
                    if target and target.endswith(".npk"):
                        file_contents[target] = content
                elif name == "default_api:replace_file_content" or name == "default_api:multi_replace_file_content":
                    # For replace we can't easily reconstruct the whole file without knowing the previous state,
                    # but maybe we can just extract the whole thing if we know it?
                    # Actually, the quickest way to recover is to checkout the git stash, wait, I didn't stash!
                    pass

print(f"Found {len(file_contents)} files written via write_to_file.")
# But wait, replace_file_content modifies them in place!
