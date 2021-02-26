#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from setuptools import setup, find_packages

setup(
    name='awsiotsdk',
    version='1.0.0-dev',
    license='License :: OSI Approved :: Apache Software License',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/aws/aws-iot-device-sdk-python-v2',
    packages=find_packages(include=['awsiot*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'awscrt==0.10.8',
    ],
    python_requires='>=3.5',
)
