# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="cm-scraper",
    version="0.1.0",
    author="Nyi Nyi Lwin",
    author_email="hello@nyinyilwin.com",
    description="A scraper for Channel Myanmar movies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/konyilwin/cm-scraper",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cm-scraper=cm.scraper:main",
        ],
    },
)