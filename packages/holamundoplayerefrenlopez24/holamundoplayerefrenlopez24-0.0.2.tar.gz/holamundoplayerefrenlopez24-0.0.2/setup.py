import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text
setuptools.setup(
    name="holamundoplayerefrenlopez24",
    version="0.0.2",
    long_description="# Player de prueba Este es un reproductor de prueba",
    packages=setuptools.find_packages(
        exclude=["mocks", "test"]
    )
)