#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="logman",
    version="0.0.2",
    author="hbjs",
    author_email="hbjs97@naver.com",
    description="logman",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WIM-Corporation/logman",
    packages=find_packages(exclude=("tests", "tests.*")),
)
