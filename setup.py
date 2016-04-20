#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='ofls-shift',
    version='1.0',
    description='Download csv file via google spread sheet, and return awesome string',
    author='masaponto',
    author_email='masaponto@gmail.com',
    url='masaponto.github.io',
    install_requires=['requests', 'pyyaml'],
    py_modules = ["ofls_shift"],
    package_dir = {'': 'src'},
    entry_points={
        'console_scripts':
            'ofls = ofls_shift:main'
    }
)
