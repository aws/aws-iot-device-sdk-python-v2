#!/usr/bin/env python

from distutils.core import setup

setup(
    name='awsiot',
    version='2.0',
    description='AWS IoT SDK based on the AWS Common Runtime',
    author='AWS SDK Common Runtime Team',
    url='https://github.com/awslabs/aws-iot-device-sdk-python-v2',
    packages = ['awsiot'],
    install_requires = ['aws_crt.mqtt']
)
