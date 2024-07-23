#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

MAJOR = 1
MINOR = 4
PATCH = 0
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


def get_install_requires():
    reqs = [
        # 'pandas>=0.18.0',
    ]
    return reqs


setup(
    name="nmake",
    version=VERSION,
    author="nagisa",
    author_email="1300296933@qq.com",
    long_description_content_type="",
    url='',
    long_description=open('README.md', encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    packages=['nmake', 'nmake.param', 'nmake.tool'],
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'': ['*.csv', '*.txt', '.toml']},  # 这个很重要
    include_package_data=True  # 也选上

)
