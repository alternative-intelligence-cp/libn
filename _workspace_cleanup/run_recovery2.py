import json
import os

transcript_path = "/home/randy/.gemini/antigravity/brain/bb1b05f1-4ffc-4162-b7d8-2f3e7de6ac97/.system_generated/logs/transcript.jsonl"
with open(transcript_path, "r") as f:
    for line in f:
        try: entry = json.loads(line)
        except: continue
        if entry.get("source") != "MODEL": continue
        for call in entry.get("tool_calls", []):
            name = call.get("name", "")
            if "replace_file_content" not in name: continue
            
            args_raw = call.get("args", call.get("arguments", {}))
            args = {}
            for k, v in args_raw.items():
                if isinstance(v, str):
                    try: args[k] = json.loads(v)
                    except: args[k] = v
                else: args[k] = v
                
            target = args.get("TargetFile")
            if not target or not os.path.exists(target): continue
            
            if "multi_replace" in name:
                chunks = args.get("ReplacementChunks", [])
                if isinstance(chunks, str):
                    try: chunks = json.loads(chunks)
                    except: chunks = []
                with open(target, "r") as tgt_f: content = tgt_f.read()
                for chunk in chunks:
                    tc = chunk.get("TargetContent")
                    if tc and tc not in content:
                        print(f"FAILED TO FIND in {os.path.basename(target)}: {repr(tc[:50])}...")
            else:
                tc = args.get("TargetContent")
                with open(target, "r") as tgt_f: content = tgt_f.read()
                if tc and tc not in content:
                    print(f"FAILED TO FIND in {os.path.basename(target)}: {repr(tc[:50])}...")
