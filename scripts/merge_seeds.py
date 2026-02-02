
import codecs
from pathlib import Path

def merge():
    files = [
        Path("db/complete_seed_2024_2026.sql"),
        Path("db/extra_seed_2025.sql")
    ]
    merged_data = ""
    for f in files:
        if not f.exists():
            print(f"File {f} not found!")
            continue
            
        print(f"Reading {f}...")
        raw = f.read_bytes()
        
        # Detect encoding
        if raw.startswith(codecs.BOM_UTF16_LE):
            content = raw.decode('utf-16-le')
        elif raw.startswith(codecs.BOM_UTF16_BE):
            content = raw.decode('utf-16-be')
        elif raw.startswith(codecs.BOM_UTF8):
            content = raw.decode('utf-8-sig')
        else:
            try:
                content = raw.decode('utf-8')
            except UnicodeDecodeError:
                content = raw.decode('latin-1')
        
        merged_data += content + "\n\n"
    
    # Clean null characters (SQLite/Python execscript doesn't like them)
    # Also ensure standard line endings
    final_data = merged_data.replace('\x00', '').replace('\r\n', '\n').replace('\r', '\n')
    
    output_path = Path("db/complete_seed_2024_2026.sql")
    print(f"Writing merged data to {output_path}...")
    output_path.write_text(final_data, encoding='utf-8')
    print("Merge complete!")

if __name__ == "__main__":
    merge()
