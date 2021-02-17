#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from setuptools import setup, find_packages

setup(
    name='awsiotsdk',
    version='1.0.0-dev',
    license='Apache-2.0',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/aws/aws-iot-device-sdk-python-v2',
    packages=find_packages(include=['awsiot*']),
    install_requires=[
        'awscrt==0.10.6',
    ],
    python_requires='>=3.5',
)
