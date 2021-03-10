#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="capcomm",
    version="0.0.1",
    author="Jared Meek",
    author_email="jm4761@columbia.edu",
    description="A package for inferring ecological community structure",
    classifiers=["Programming Language :: Python :: 3"],
#   entry_points={
#        "console_scripts": ["capcomm = capcomm.__main__:main"]
#   },
)
