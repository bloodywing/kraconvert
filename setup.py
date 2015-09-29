# -*- coding: utf-8 -*-


import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import kraconvert

packages = [
    'kraconvert',
]

entry_points = {
    'console_scripts': [
        'kraconvert = kraconvert.main:run',
    ]
}

package_data = {

}

requires = [
    'lxml'
]

setup(
    name='kraconvert',
    version=kraconvert.__version__,
    description='Konverts Krita .kra files onto something',
    packages=packages,
    package_data=package_data,
    entry_points=entry_points,
    install_requires=requires,
    author='pierre',
    author_email='pierre@isartistic.biz',
    license='CC0',
)