#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from setuptools import setup

setup(
    name='awsiotsdk',
    version='1.0.0-dev',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/aws/aws-iot-device-sdk-python-v2',
    packages = ['awsiot'],
    install_requires=[
        'awscrt==0.6.2',
        'futures;python_version<"3.2"',
        'typing;python_version<"3.5"',
    ],
    python_requires='>=2.7',
)
