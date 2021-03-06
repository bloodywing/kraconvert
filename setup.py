try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import kraconvert
import os

packages = [
    'kraconvert',
]

entry_points = {
    'console_scripts': [
        'kraconvert = kraconvert.main:main',
    ]
}

package_data = {
    'kraconvert': ['files/*.icc']
}

requires = [
    'lxml', 'pillow'
]

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.md'))
long_description = f.read().strip()
f.close()

setup(
    name='kraconvert',
    version=kraconvert.__version__,
    description='Konverts Krita .kra files into PNG and JPEG.',
    url='https://github.com/bloodywing/kraconvert',
    packages=packages,
    package_data=package_data,
    entry_points=entry_points,
    install_requires=requires,
    requires=requires,
    long_description=long_description,
    author='Pierre Geier <bloodywing>',
    author_email='pierre@isartistic.biz',
    download_url='https://github.com/bloodywing/kraconvert/tarball/{tag}'.format(tag=kraconvert.__version__),
    license='CC0',
    keywords=['experimental', 'krita', 'converter', 'tool', 'utility'],
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Utilities',
    ]
)