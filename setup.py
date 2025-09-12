# -*- coding: utf-8 -*-
"""Builds package for release."""
import os
from setuptools import setup, find_packages
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='bakzip',
    version='0.1',
    packages=find_packages(),
    description=("Simple cli based backup tool" 
                 " This provide encryption, compression and skipping capabilities to skip dev file."),
    long_description=read('README.md'),
    author='Smx27',
    author_email='smx27@github.com',
    license='MIT',
    install_requires=[
        'pyzipper',
        'pyfiglet',
        'pytest',
        'rich',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'bakzip=bakzip.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
       "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8"
)
