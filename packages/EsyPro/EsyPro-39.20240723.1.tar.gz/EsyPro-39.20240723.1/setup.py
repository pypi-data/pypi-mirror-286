# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='EsyPro',
            version='39.20240723.1',
            packages=['EsyPro',],
            description='a python lib for project files',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.*'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            