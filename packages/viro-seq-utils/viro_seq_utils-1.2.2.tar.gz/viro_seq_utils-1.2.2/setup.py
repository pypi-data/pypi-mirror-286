#! /usr/bin/env python

"""
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 22 jan. 2020
"""

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viro-seq-utils",
    version="1.2.2",
    author="Nicolas Jeanne",
    author_email="jeanne.n@chu-toulouse.fr",
    description="Utilities modules for sequences, alignments and phylogeny from Toulouse virology laboratory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BioDReD/python-package-viro-seq-utils",
    project_urls={
        "Bug Tracker": "https://github.com/BioDReD/python-package-viro-seq-utils/issues",
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    keywords="alignment sequence phylogeny",
    license="GNU General Public License",
    install_requires=["biopython==1.84", "numpy==1.26.1"]
)
