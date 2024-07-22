import argparse
import os
from exereverse.extractor import extract_executable

def main():
    parser = argparse.ArgumentParser(description="Extract PyInstaller executable")
    parser.add_argument("--file", required=True, help="Path to the PyInstaller executable")
    parser.add_argument("--path", help="Path to save the extracted files (default: ./extracted_files)")
    args = parser.parse_args()

    exe_file = args.file
    output_dir = args.path if args.path else "extracted_files"

    extract_executable(exe_file, output_dir)

    print(f"Extracted files are saved in: {output_dir}")

if __name__ == "__main__":
    main()
