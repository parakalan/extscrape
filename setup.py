# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 23:28:21 2017

@author: sudharsan
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

req_list = ['tqdm', 'requests', 'lxml']

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name='extscraper',

    packages=['extscraper'],

    version='1.0.0',

    description='Scrapes files from the web'
    ' with specified extensions.',

    author='Sudharshan',

    author_email='stsudharshan@gmail.com',

    install_requires=req_list,

    entry_points={
        'console_scripts': ['extscraper = extscraper:'
                            'main']
    },

    url='',

    keywords=['scrape', 'extension'],

    classifiers=['Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Education'],

    license='MIT License'
)
