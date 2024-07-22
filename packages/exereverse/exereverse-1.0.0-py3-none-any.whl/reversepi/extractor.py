import subprocess
import sys
import os

def install_package(package):
    print(f"Installing {package}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def ensure_tools():
    try:
        import uncompyle6
    except ImportError:
        install_package("uncompyle6")

    pyinstxtractor_path = os.path.join(os.path.dirname(__file__), "pyinstxtractor.py")
    if not os.path.isfile(pyinstxtractor_path):
        print(f"pyinstxtractor.py not found in {pyinstxtractor_path}. Downloading...")
        download_file("https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py", pyinstxtractor_path)

def download_file(url, dest):
    import urllib.request
    print(f"Downloading {url} to {dest}...")
    urllib.request.urlretrieve(url, dest)

def extract_executable(exe_file):
    ensure_tools()
    pyinstxtractor_path = os.path.join(os.path.dirname(__file__), "pyinstxtractor.py")
    print(f"Extracting {exe_file}...")
    subprocess.run([sys.executable, pyinstxtractor_path, exe_file], check=True)
