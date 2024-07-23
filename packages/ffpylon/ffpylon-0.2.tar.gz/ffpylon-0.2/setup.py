#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: setup.py
@DateTime: 2024/1/28 18:50
@SoftWare: 
"""

from setuptools import setup, find_packages


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name='ffpylon',
    version='0.2',
    keywords=['ffpylon', 'ffmpeg'],
    packages=find_packages(),
    package_data={"": ["LICENSE", "NOTICE"]},
    include_package_data=True,
    author="nickdecodes",
    author_email="nickdecodes@163.com",
    description="FFPylon Package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=[
        'twine',
        'build',
        'installer'
    ],
    project_urls={
        "Documentation": "http://python-ffpylon.readthedocs.io",
        "Source": "https://github.com/nickdecodes/python-ffpylon",
    },
    license='Apache License 2.0'
)
