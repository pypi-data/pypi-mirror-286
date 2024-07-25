from setuptools import setup, find_packages
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name = "pyrisks",
    version = "0.1.3",
    description = "...",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    author = "Andres Felipe Rico, Diego Nicolas Rozo, Juan Camilo Martinez, Nicolas Ricardo Lopez, Lucas Gómez Tobón, William Andres Sanchez",
    author_email = "lucasgomeztobon@gmail.com, ",
    license = "MIT",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages = ["pyrisks"],
    include_package_data = True,
    package_data = {
        # Include any .xlsx files within the 'data' directory
        'pyrisks': ['data/*.xlsx'],
    },
    install_requires = [
        "numpy",
        "pandas",
        ]
)