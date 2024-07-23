"""
This project is a simple unit converter.
"""

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

setup(
    name="unit_converter_python",
    version="0.0.1",
    author="Daniel Torres de Andrade",
    author_email="danieltorresandrade@gmail.com",
    description="This project is a simple unit converter.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Danieltandrade/Unit-Converter",
    packages=find_packages(),
    license="MIT License",
    keywords="unit converter, unit-converter, unit_converter",
    python_requires='>=3.12',
)
