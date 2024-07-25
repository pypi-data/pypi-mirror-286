# -*- encoding: utf8 -*-
import os
import sys

def create_package_structure(package_name):
    """Create a basic Python package structure."""
    dirs = [package_name, 'tests'] # 'package'
    files = [('setup.py', setup_py_content(package_name)), 
             ('README.md', read_me_content()), 
             ('requirements.txt', '')]

    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)

    for file_name, content in files:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)

def setup_py_content(package_name):
    return f"""
# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{package_name}",
    version="0.1.0",
    author="example",
    author_email="example@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/{package_name}",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
"""

def read_me_content():
    return "# Package Name\n\nA brief description of your package."

if __name__ == "__main__":
    if "commands" in sys.argv:
        print("python setup.py sdist")
        print("python setup.py bdist_wheel")
        sys.exit(0)
    try:
        print("[%] Python PIP Package Builder")
        package_name = input("Enter the name of your package: ")
        create_package_structure(package_name)
        print(f"Package structure created for '{package_name}'.")
    except Exception as e:
        print(f"[^] Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
        sys.exit(0)

