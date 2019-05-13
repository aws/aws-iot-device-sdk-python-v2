#!/usr/bin/env python

# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from setuptools import setup, find_packages

setup(
    name='awsiotsdk',
    version='0.2.4',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/awslabs/aws-iot-device-sdk-python-v2',
    packages = find_packages(),
    install_requires=[
        'awscrt==0.2.16',
        'futures; python_version == "2.7"',
        'typing; python_version <= "3.4"',
    ],
    python_requires='>=2.7',
)
