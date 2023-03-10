# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
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
        warnings.simplefilter('ignore', ResourceWarning)

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

    def _run(self, args, stdout_checker):
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode()
        try:
            self.assertEqual(0, process.returncode)
            stdout_checker(stdout)
        except Exception as e:
            # print output and rethrow exception
            print(subprocess.list2cmdline(args))
            print("--- stdout ---")
            for line in stdout.splitlines():
                print(line)
            print("--- stderr ---")
            for line in stderr.splitlines():
                print(line)
            print("--- end ---")

            raise e

    def test_pubsub(self):
        config = Config.get()
        args = [
            sys.executable,
            "samples/pubsub.py",
            "--endpoint", config.endpoint,
            "--cert", config.cert_filepath,
            "--key", config.key_filepath,
            "--client_id", create_client_id(),
            "--count", "1",
            "--verbosity", "Trace",
        ]

        def stdout_checker(stdout):
            # check for last line printed by sample
            last_line = stdout.splitlines()[-1]
            self.assertTrue(last_line.startswith("Disconnected!"))

        self._run(args, stdout_checker)

    def test_basic_discovery_response_only(self):
        config = Config.get()
        args = [
            sys.executable,
            "samples/basic_discovery.py",
            "--print_discover_resp_only",
            "--region", config.region,
            "--cert", config.cert_filepath,
            "--key", config.key_filepath,
            "--thing_name", "aws-sdk-crt-unit-test",
            "--verbosity", "Trace",
        ]

        def stdout_checker(stdout):
            # check for last line printed by sample
            last_line = stdout.splitlines()[-1]
            self.assertTrue(last_line.startswith("awsiot.greengrass_discovery.DiscoverResponse("))

        self._run(args, stdout_checker)
