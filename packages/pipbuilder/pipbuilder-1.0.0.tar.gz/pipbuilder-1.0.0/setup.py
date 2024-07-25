
# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipbuilder",
    version="1.0.0",
    author="YELANDAOKONG",
    author_email="YELANDAOKONG@yldk.xyz",
    description="Python PIP Package Builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YELANDAOKONG/pipbuilder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
