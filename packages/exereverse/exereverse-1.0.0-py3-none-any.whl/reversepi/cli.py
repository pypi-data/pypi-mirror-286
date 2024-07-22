import argparse
import os
import subprocess
from reversepi.extractor import extract_executable
from reversepi.decompiler import decompile_pyc_files

def main():
    parser = argparse.ArgumentParser(description="Extract and decompile PyInstaller executable")
    parser.add_argument("--file", required=True, help="Path to the PyInstaller executable")
    parser.add_argument("--path", help="Path to save the decompiled files (default: ./decompiled_code)")
    args = parser.parse_args()

    exe_file = args.file
    output_dir = args.path if args.path else "decompiled_code"

    extracted_dir = exe_file + "_extracted"
    os.makedirs(output_dir, exist_ok=True)

    extract_executable(exe_file)
    decompile_pyc_files(extracted_dir, output_dir)

    print(f"Decompiled files are saved in: {output_dir}")

if __name__ == "__main__":
    main()
