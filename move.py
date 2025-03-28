# move_files.py
import os
import shutil

# The folder that currently has the files you want to move
source_dir = "frontend"

# The destination folder (the parent "overtime" directory)
dest_dir = "."

# The files you want to move
files_to_move = ["app.py", "backend.py", "database.py", "setup.py"]

for filename in files_to_move:
    src_path = os.path.join(source_dir, filename)
    dst_path = os.path.join(dest_dir, filename)
    
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
        print(f"Moved {src_path} -> {dst_path}")
    else:
        print(f"Skipping {src_path}; file not found.")
