import os
import urllib.request

def download_file(url, dest):
    print(f"Downloading {url} to {dest}...")
    urllib.request.urlretrieve(url, dest)

def main():
    pyinstxtractor_path = os.path.join(os.path.dirname(__file__), "pyinstxtractor.py")
    if not os.path.isfile(pyinstxtractor_path):
        download_file("https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py", pyinstxtractor_path)
    else:
        print("pyinstxtractor.py already exists.")

if __name__ == "__main__":
    main()
