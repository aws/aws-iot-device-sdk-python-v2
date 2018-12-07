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

from distutils.core import setup

setup(
    name='awsiot',
    version='2.0',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/awslabs/aws-iot-device-sdk-python-v2',
    packages = ['awsiot'],
    install_requires=['aws_crt.mqtt'],
    python_requires='>=2.7',
)
