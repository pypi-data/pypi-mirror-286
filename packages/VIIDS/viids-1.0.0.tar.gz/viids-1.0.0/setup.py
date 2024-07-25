from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="VIIDS",
    version="1.0.0",
    author="VII Data Science",
    description="VII Data Science Internship bundle of useful functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
)