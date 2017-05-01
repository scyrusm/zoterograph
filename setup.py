#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os
#import re

from setuptools import setup, find_packages


classifiers = """\
    Development Status :: 4 - Beta
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 2
"""





install_requires = [
    'selenium', 
    'threading',
    'SimpleHTTPServer',
    'SocketServer',
    'json',
    'time',
    'pyzotero',
]





setup(
    name='zoterograph',
    author='Samuel Markson',
    author_email='scmarkson@gmail.com',
    version='0.1',
    license='BSD3',
    description='Package for visualization of zotero bibliography',
    keywords=['zotero'],
  #  url='https://github.com/mirnylab/cooler',
    packages=['zoterograph'],
    package_data={'zoterograph':['/data/*']},
    install_requires=install_requires
#    entry_points={
#        'console_scripts': [
#            'cooler = cooler.cli:cli',
#        ]
#    }
)
