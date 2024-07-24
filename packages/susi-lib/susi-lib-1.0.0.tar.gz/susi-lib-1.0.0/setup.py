from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="susi-lib",
    version="1.0.0",
    description="Library for SuŠi organizers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olilag/susi-lib",
    author="Oliver Lago",
    author_email="oliver.oli.lago@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
)
