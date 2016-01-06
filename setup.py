#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_info(name):
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'restart_wechat/__init__.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals[name]


setup(
    name='RESTArt-WeChat',
    version=get_info('__version__'),
    author=get_info('__author__'),
    author_email=get_info('__email__'),
    maintainer=get_info('__author__'),
    maintainer_email=get_info('__email__'),
    keywords='WeChat, RESTArt, Python',
    description=get_info('__doc__'),
    license=get_info('__license__'),
    long_description=get_info('__doc__'),
    packages=find_packages(exclude=['tests']),
    url='https://github.com/RussellLuo/restart-wechat',
    install_requires=[
        'python-restart',
        'wechatpy',
        'cryptography',
    ],
)
