__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "23.07.2024"
__email__ = "m@hler.eu"
__status__ = "Development"

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cs2inspect",
    version="0.0.1",
    author="Lukas Mahler",
    author_email="m@hler.eu",
    description="CS2 inspect link utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Helyux/cs2inspect",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
