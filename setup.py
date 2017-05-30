#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='ofls',
    version='2.0',
    description='Print shift table of OFLS',
    author='masaponto',
    author_email='masaponto@gmail.com',
    url='masaponto.github.io',
    install_requires=['requests', 'Ptable'],
    py_modules=["ofls"],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts':
            'ofls = ofls:main'
    }
)
