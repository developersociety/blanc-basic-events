#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name='blanc-basic-events',
    version='0.3.3',
    description='Blanc Basic Events for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/blanc-basic-events',
    maintainer='Blanc Ltd',
    maintainer_email='studio@blanc.ltd.uk',
    platforms=['any'],
    install_requires=[
        'blanc-basic-assets>=0.3',
        'icalendar>=3.6',
    ],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
)
