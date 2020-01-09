# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License').
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the 'license' file accompanying this file. This file is distributed
# on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from __future__ import absolute_import, print_function
import awsiot
import boto3
import botocore.exceptions
import os.path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
import warnings


class Config:
    cache = None

    def __init__(self, endpoint, cert, key, region):
        self.endpoint = endpoint
        self.region = region
        self.cert_bytes = cert
        self.key_bytes = key

        self._tmp_dirpath = tempfile.mkdtemp()
        self.cert_filepath = os.path.join(self._tmp_dirpath, 'certificate.pem')
        with open(self.cert_filepath, 'wb') as cert_file:
            cert_file.write(cert)

        self.key_filepath = os.path.join(self._tmp_dirpath, 'privatekey.pem')
        with open(self.key_filepath, 'wb') as key_file:
            key_file.write(key)

    def __del__(self):
        shutil.rmtree(self._tmp_dirpath)

    @staticmethod
    def get():
        """Raises SkipTest if credentials aren't set up correctly"""
        if Config.cache:
            return Config.cache

        # boto3 caches the HTTPS connection for the API calls, which appears to the unit test
        # framework as a leak, so ignore it, that's not what we're testing here
        try:
            warnings.simplefilter('ignore', ResourceWarning)
        except NameError:  # Python 2 has no ResourceWarning
            pass

        try:
            secrets = boto3.client('secretsmanager')
            response = secrets.get_secret_value(SecretId='unit-test/endpoint')
            endpoint = response['SecretString']
            response = secrets.get_secret_value(SecretId='unit-test/certificate')
            cert = response['SecretString'].encode('utf8')
            response = secrets.get_secret_value(SecretId='unit-test/privatekey')
            key = response['SecretString'].encode('utf8')
            region = secrets.meta.region_name
            Config.cache = Config(endpoint, cert, key, region)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as ex:
            raise unittest.SkipTest("No credentials")

        return Config.cache


def create_client_id():
    return 'aws-crt-python-unit-test-{0}'.format(uuid.uuid4())


class SamplesTest(unittest.TestCase):

    def _run(self, args):
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # only print output if test failed
        if process.returncode != 0:
            print(subprocess.list2cmdline(args))
            print("--- stdout ---")
            for line in stdout.splitlines():
                print(line)
            print("--- stderr ---")
            for line in stderr.splitlines():
                print(line)
            print("--- end ---")

        self.assertEquals(0, process.returncode)
        return stdout

    def test_pubsub(self):
        config = Config.get()
        args = [
            sys.executable,
            "samples/pubsub.py",
            "--endpoint", config.endpoint,
            "--cert", config.cert_filepath,
            "--key", config.key_filepath,
            "--client-id", create_client_id(),
            "--count", "1",
            #"--verbosity", "Trace",
        ]
        stdout = self._run(args)
        self.assertTrue(stdout.endswith("Disconnected!\n"))

    def test_basic_discovery_response_only(self):
        config = Config.get()
        args = [
            sys.executable,
            "samples/basic_discovery.py",
            "--print-discover-resp-only",
            "--region", config.region,
            "--cert", config.cert_filepath,
            "--key", config.key_filepath,
            "--thing-name", "aws-sdk-crt-unit-test",
            "-v", "Trace",
        ]
        stdout = self._run(args)
        self.assertTrue("\nawsiot.greengrass_discovery.DiscoverResponse(" in stdout)
