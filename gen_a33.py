import os

def generate_compilation(output_file, build_output_file):
    project_dir = "/home/randy/Workspace/REPOS/libn"
    src_dir = os.path.join(project_dir, "src")
    
    with open(output_file, 'w') as out_f:
        out_f.write("# Source Files Compilation\n\n")
        
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".npk") or file.endswith(".s") or file.endswith(".abc"):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, project_dir)
                    
                    out_f.write(f"================================================================================\n")
                    out_f.write(f"File: {relpath}\n")
                    out_f.write(f"================================================================================\n\n")
                    
                    try:
                        with open(filepath, 'r') as in_f:
                            content = in_f.read()
                            out_f.write(content)
                            if not content.endswith('\n'):
                                out_f.write('\n')
                    except Exception as e:
                        out_f.write(f"// Error reading file: {e}\n")
                    
                    out_f.write("\n")
        
        # Build file
        build_file = os.path.join(project_dir, "build.abc")
        if os.path.exists(build_file):
            out_f.write(f"================================================================================\n")
            out_f.write(f"File: build.abc\n")
            out_f.write(f"================================================================================\n\n")
            with open(build_file, 'r') as in_f:
                content = in_f.read()
                out_f.write(content)
                if not content.endswith('\n'):
                    out_f.write('\n')
            out_f.write("\n")

        # Build output
        out_f.write("================================================================================\n")
        out_f.write("Build Output\n")
        out_f.write("================================================================================\n\n")
        
        if os.path.exists(build_output_file):
            with open(build_output_file, 'r') as b_f:
                out_f.write(b_f.read())
        else:
            out_f.write("No build output found.\n")

if __name__ == "__main__":
    import sys
    generate_compilation(sys.argv[1], sys.argv[2])
