from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import sys

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        pyinstxtractor_path = os.path.join(os.path.dirname(__file__), "exereverse", "pyinstxtractor.py")
        if not os.path.isfile(pyinstxtractor_path):
            subprocess.run([sys.executable, "exereverse/post_install.py"], check=True)

setup(
    name="exereverse",
    version="1.1.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "exereverse=exereverse.cli:main",
        ],
    },
    include_package_data=True,
    description="A tool to extract PyInstaller executables",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ByteBreach/exereverse",
    author="MrFida",
    author_email="mrfidal@proton.me",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': PostInstallCommand,
    },
)
