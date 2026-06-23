import json
import os

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
            args_raw = call.get("arguments", {})
            if isinstance(args_raw, str):
                try:
                    args = json.loads(args_raw)
                except:
                    args = {}
            else:
                args = args_raw
                
            if "replace_file_content" in name:
                target = args.get("TargetFile")
                if not target: continue
                
                if name.endswith("multi_replace_file_content"):
                    chunks = args.get("ReplacementChunks", [])
                    if os.path.exists(target):
                        with open(target, "r") as tgt_f:
                            content = tgt_f.read()
                        changed = False
                        for chunk in chunks:
                            tc = chunk.get("TargetContent")
                            rc = chunk.get("ReplacementContent")
                            if tc and tc in content:
                                content = content.replace(tc, rc)
                                changed = True
                        if changed:
                            with open(target, "w") as tgt_f:
                                tgt_f.write(content)
                            print(f"Recovered multi-edit for {target}")
                else:
                    tc = args.get("TargetContent")
                    rc = args.get("ReplacementContent")
                    if os.path.exists(target):
                        with open(target, "r") as tgt_f:
                            content = tgt_f.read()
                        if tc and tc in content:
                            with open(target, "w") as tgt_f:
                                tgt_f.write(content.replace(tc, rc))
                            print(f"Recovered edit for {target}")

