# -*- coding: utf-8 -*-
"""
File: setup.py
Author: Rinat F Sabitov
Description: smyt task
"""

import sys
import os
from setuptools import setup, find_packages

root_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root_dir, 'src'))

version = __import__('task').get_version()


def read(fname):
    """ Attempt to read a file and return it's content as a text
    """
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="task",
    version=version,
    description=read('DESCRIPTION'),
    author="Rinat Sabitov",
    url="https://spot.falseprotagonist.me:8081",
    package_dir={'': 'src'},
    packages=find_packages("src"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=read('REQUIREMENTS'),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.md'),
    test_suite='test',
    tests_request=['nose', ]
)
