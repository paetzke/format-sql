# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from setuptools import find_packages, setup

setup(name='format-sql',
      py_modules=['format_sql'],
      description='format-sql is a tool to format SQL in your Python strings!',
      long_description=(open('README.rst').read()),
      version='0.1.0',
      license='BSD',
      author='Friedrich Paetzke',
      author_email='paetzke@fastmail.fm',
      url='https://github.com/paetzke/format-sql',
      packages=find_packages(exclude=['tests*']),
      install_requires=open('requirements/package.txt').read().splitlines(),
      entry_points={
          'console_scripts': ['format-sql = format_sql.main:main']
      },
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
      ])
