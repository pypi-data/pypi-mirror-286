#!/usr/bin/env python

# Copyright (c) 2014 SeatGeek

# This file is part of thefuzz.

from thefuzz import __version__
from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="the_fuzz_with_custom_object",
    version=__version__,
    author="Adam Cohen & z1kurat",
    author_email="z1kuratdeveloper@gmail.com",
    packages=["thefuzz"],
    # keep for backwards compatibility of projects depending on `thefuzz[speedup]`
    extras_require={"speedup": []},
    install_requires=["rapidfuzz>=3.0.0, < 4.0.0"],
    url="https://github.com/z1kurat/thefuzz",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    description="Fuzzy String Matching with custom objects in Python",
    long_description=long_description,
    zip_safe=True,
    python_requires=">=3.8",
)
