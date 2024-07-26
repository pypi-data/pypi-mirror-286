#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:45:48 2024

@author: cameronmeharry
"""

from setuptools import setup, find_packages

setup(
    name='pyk_pack',
    version='0.3.0',
    package_dir={'': 'src'},
    packages=find_packages(where = 'src'),
    package_data={
        'pyk_pack': ['*.csv'],
    },
    # other setup parameters...
)