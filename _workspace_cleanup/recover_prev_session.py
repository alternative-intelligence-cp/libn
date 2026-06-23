import json
import os

transcript_path = "/home/randy/.gemini/antigravity/brain/e746eed2-1ee9-4904-9a6b-0a9d69653bf8/.system_generated/logs/transcript.jsonl"
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
            args = call.get("arguments", {})
            
            if name == "default_api:replace_file_content":
                target = args.get("TargetFile")
                target_content = args.get("TargetContent")
                repl_content = args.get("ReplacementContent")
                
                if target and os.path.exists(target):
                    with open(target, "r") as tgt_f:
                        content = tgt_f.read()
                    if target_content in content:
                        with open(target, "w") as tgt_f:
                            tgt_f.write(content.replace(target_content, repl_content))
                        print(f"Recovered edit for {target}")
            
            elif name == "default_api:multi_replace_file_content":
                target = args.get("TargetFile")
                chunks = args.get("ReplacementChunks", [])
                
                if target and os.path.exists(target):
                    with open(target, "r") as tgt_f:
                        content = tgt_f.read()
                        
                    changed = False
                    for chunk in chunks:
                        target_content = chunk.get("TargetContent")
                        repl_content = chunk.get("ReplacementContent")
                        if target_content and target_content in content:
                            content = content.replace(target_content, repl_content)
                            changed = True
                    if changed:
                        with open(target, "w") as tgt_f:
                            tgt_f.write(content)
                        print(f"Recovered multi-edit for {target}")
                        
            elif name == "default_api:run_command":
                cmd = args.get("CommandLine", "")
                if cmd.startswith("cat << 'EOF' >"):
                    print(f"Executing: {cmd[:50]}...")
                    os.system(cmd)
