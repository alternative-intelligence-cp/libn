import glob
import re

for filepath in glob.glob('src/io/bio/*.npk'):
    with open(filepath, 'r') as f:
        text = f.read()
        
    # Casts
    text = re.sub(r'([A-Za-z0-9_.]+)\s+as\s+\*FILE', r'@cast_unchecked<FILE->>(\1)', text)
    text = re.sub(r'\(([^)]+)\)\s+as\s+\*FILE', r'@cast_unchecked<FILE->>(\1)', text)
    text = re.sub(r'([A-Za-z0-9_.]+)\s+as\s+\*byte', r'@cast_unchecked<uint8->>(\1)', text)
    text = re.sub(r'\(([^)]+)\)\s+as\s+\*byte', r'@cast_unchecked<uint8->>(\1)', text)
    text = re.sub(r'([A-Za-z0-9_.]+)\s+as\s+\*int64', r'@cast_unchecked<int64->>(\1)', text)
    text = re.sub(r'\(([^)]+)\)\s+as\s+\*int64', r'@cast_unchecked<int64->>(\1)', text)
    text = re.sub(r'&\s*([A-Za-z0-9_\[\]]+)\s+as\s+int64', r'@cast_unchecked<int64>(&\1)', text)
    text = re.sub(r'([A-Za-z0-9_.]+)\s+as\s+int64', r'@cast_unchecked<int64>(\1)', text)
    text = re.sub(r'([A-Za-z0-9_.]+)\s+as\s+byte', r'@cast_unchecked<uint8>(\1)', text)
    
    # Declarations
    text = re.sub(r'\*FILE:([A-Za-z0-9_]+)', r'FILE->:\1', text)
    text = re.sub(r'\*byte:([A-Za-z0-9_]+)', r'uint8->:\1', text)
    text = re.sub(r'\*int64:([A-Za-z0-9_]+)', r'int64->:\1', text)
    
    # Error fields
    text = re.sub(r'\.err\b', '.error', text)
    
    # Fail casts
    text = re.sub(r'fail ([A-Za-z0-9_]+) as tbb8;', r'fail \1;', text)
    
    # Function calls implicitly evaluating to Result
    # Any call to another function inside bio that evaluates to int64 needs `raw` if inside a fallible function.
    # To be safe, we will manually add raw to the ones throwing errors.
    
    with open(filepath, 'w') as f:
        f.write(text)

