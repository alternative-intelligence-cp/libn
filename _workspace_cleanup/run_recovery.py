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
            
        for call in entry.get("tool_calls", []):
            name = call.get("name", "")
            if "replace_file_content" not in name:
                continue
                
            args_raw = call.get("args", call.get("arguments", {}))
            
            # Parse stringified JSON values
            args = {}
            for k, v in args_raw.items():
                if isinstance(v, str):
                    try:
                        args[k] = json.loads(v)
                    except:
                        args[k] = v
                else:
                    args[k] = v
                    
            target = args.get("TargetFile")
            if not target or not os.path.exists(target):
                continue
                
            if "multi_replace" in name:
                chunks = args.get("ReplacementChunks", [])
                if isinstance(chunks, str):
                    try: chunks = json.loads(chunks)
                    except: chunks = []
                
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
                with open(target, "r") as tgt_f:
                    content = tgt_f.read()
                if tc and tc in content:
                    with open(target, "w") as tgt_f:
                        tgt_f.write(content.replace(tc, rc))
                    print(f"Recovered edit for {target}")

