#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import codecs
import re
import os
from setuptools import setup, find_packages

VERSION_RE = re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S)
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))


def _load_readme():
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with codecs.open(readme_path, 'r', 'utf-8') as f:
        return f.read()


def _load_version():
    init_path = os.path.join(PROJECT_DIR, 'awsiot', '__init__.py')
    with open(init_path) as fp:
        return VERSION_RE.match(fp.read()).group(1)


setup(
    name='awsiotsdk',
    version=_load_version(),
    license='License :: OSI Approved :: Apache Software License',
    description='AWS IoT SDK based on the AWS Common Runtime',
    long_description=_load_readme(),
    long_description_content_type='text/markdown',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/aws/aws-iot-device-sdk-python-v2',
    packages=find_packages(include=['awsiot*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'awscrt==0.16.0',
    ],
    python_requires='>=3.7',
)
