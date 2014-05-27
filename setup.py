#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='blanc-basic-events',
    version='0.2.7',
    description='Blanc Basic Events for Django',
    long_description=open('README.rst').read(),
    url='http://www.blanctools.com/',
    maintainer='Alex Tomkins',
    maintainer_email='alex@hawkz.com',
    platforms=['any'],
    install_requires=[
        'icalendar>=3.6',
    ],
    packages=[
        'blanc_basic_events',
        'blanc_basic_events.templatetags',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD-2',
)
