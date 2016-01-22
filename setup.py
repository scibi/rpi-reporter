#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import setuptools

setuptools.setup(
    name="rpi-reporter",
    version="0.1.0",
    url="https://github.com/scibi/rpi-reporter",

    author="Patryk Ściborek",
    author_email="patryk@sciborek.com",

    description="Daemon which sends temperature data to statsd server",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'requests',
        'six',
        'statsd',
        'w1thermsensor',
    ],
    entry_points={
        'console_scripts': ['rpi_reporter=rpi_reporter.main:main'],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
