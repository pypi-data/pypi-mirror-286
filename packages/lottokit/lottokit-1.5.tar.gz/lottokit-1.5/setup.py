#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: setup.py
@DateTime: 2024/1/28 18:50
@SoftWare: 
"""

from setuptools import setup, find_packages


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name='lottokit',
    version='1.5',
    keywords=['lottokit', 'lottery'],
    packages=find_packages(),
    package_data={"": ["LICENSE", "NOTICE"]},
    include_package_data=True,
    author="nickdecodes",
    author_email="nickdecodes@163.com",
    description="Lotto Kit Package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=[
        'selenium>=4.11.2',
        'webdriver_manager>=4.0.0',
        'pandas>=2.0.3',
        'numpy>=1.24.3',
        'statsmodels>=0.14.0',
        'Pillow>=9.5.0',
        'scikit-learn>=1.3.2',
        'pmdarima>=2.0.4',
        'pywavelets>=1.6.0',
        'requests',
        'twine>=4.0.2',
        'build>=1.2.1',
        'installer>=0.7.0'
    ],
    project_urls={
        "Documentation": "http://python-lottokit.readthedocs.io",
        "Source": "https://github.com/nickdecodes/python-lottokit",
    },
    license='Apache License 2.0'
)
