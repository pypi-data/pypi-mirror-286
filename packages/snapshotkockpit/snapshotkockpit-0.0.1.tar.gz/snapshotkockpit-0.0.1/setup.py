from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.1'
DESCRIPTION = 'A library for creating snapshots of data over specified date ranges using Spark.'
with open('README.md',"r") as fh:
    LONG_DESCRIPTION=fh.read()

# Setting up
setup(
    name="snapshotkockpit",
    version=VERSION,
    author="Naveen Gulati, Shubham Rawat",
    author_email="gulati1432@gmail.com, rawatshubham71@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Snapshot', 'pyspark', 'Naveen Gulati', 'Shubham Rawat'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

