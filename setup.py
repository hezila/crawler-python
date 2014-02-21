#!/usr/bin/env python

from setuptools import setup, find_packages
import sys
sys.path.insert(0, '.')

setup(name='crawler-python',
      version='1.0',
      license='BSD',
      description='Python Crawler',
      author='Feng Wang',
      author_email='wffrank1987@gmail.com',
      download_url='https://github.com/numb3r3/crawler-python',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      )
