import setuptools
from pathlib import Path
setuptools.setup(
    name="jechmx",
    version="0.0.0",
    long_description=Path("readme.md").read_text(encoding="utf-8"),
    packages=setuptools.find_packages(exclude=["mocks", "tests"])
)
