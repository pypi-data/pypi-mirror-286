from setuptools import setup, find_packages
from pathlib import Path
long_desc = Path("README.md").read_text(encoding="utf-8")
setup(
    name="jechmx",
    long_description=long_desc,
    author="Jose Emmanuel Chavez",
    author_email="jechmx1@gmail.com",
    version="1.0.0"
)
