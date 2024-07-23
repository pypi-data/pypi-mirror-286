from setuptools import setup, find_packages
from os import path

name = "pandas-dataset"
version = "0.1.4"
description = "Python Datasets on top of Pandas"
url = "https://gitlab.com/meehai/pandas-dataset"

loc = path.abspath(path.dirname(__file__))
with open(f"{loc}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required = ["pandas==2.0.1", "numpy>=1.24.1,<2.0.0", "loggez==0.3", "pyarrow==11.0.0", "natsort==8.4.0",
            "lovely-tensors==0.1.15", "torch>=2.2.1"]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=find_packages(),
    install_requires=required,
    dependency_links=[],
    license="WTFPL",
    python_requires=">=3.8"
)
