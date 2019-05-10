# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import boto3
import base64
import os
import argparse
from botocore.exceptions import ClientError


def get_secret(stage):

    secret_name = '{}/aws-crt-python/.pypirc'.format(stage)
    region_name = 'us-east-1'

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret = None
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        secret = decoded_binary_secret

    with open(os.path.join(os.path.expanduser('~/'), '.pypirc'), 'w') as f:
        f.write(secret)

    print('.pypirc written to {}'.format(os.path.join(os.path.expanduser('~/'), '.pypirc')))

parser = argparse.ArgumentParser()
parser.add_argument('stage', help='Stage to deploy the pypi package to (e.g. alpha, prod, etc...)', type=str)
args = parser.parse_args()
get_secret(args.stage)
    
