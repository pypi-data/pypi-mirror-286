import subprocess
import glob
import os

def decompile_pyc_files(extracted_dir, output_dir):
    pyc_files = glob.glob(os.path.join(extracted_dir, "**/*.pyc"), recursive=True)
    if not pyc_files:
        print("No .pyc files found to decompile.")
        return
    
    print("Decompiling .pyc files...")
    for pyc_file in pyc_files:
        subprocess.run(["uncompyle6", "-o", output_dir, pyc_file], check=True)
