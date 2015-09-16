#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as f:
        return f.read()

setup(
    name = "pywiring",
    version = "0.1",
    author = "Davide Depau",
    author_email = "apps@davideddu.org",
    description = ("A module tries to bring a Wiring-like interface to Python."),
    license = "GPLv2",
    keywords = "wiring i2c gpio parallel serial io",
    url = "http://github.com/Davidedd/python-pywiring",
    packages=['pywiring'],
    long_description=read('README.md'),
    requires=["smbus", "parallel", "numpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
