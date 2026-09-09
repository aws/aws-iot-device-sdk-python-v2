# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import os
import unittest
import uuid
import warnings
from unittest.mock import patch

import boto3
import botocore.exceptions

import awscrt.io
import awscrt.mqtt
import awscrt.mqtt5

from awsiot import mqtt_connection_builder, mqtt5_client_builder
from awsiot._iot_metrics import (
    _IOT_SDK_METRICS_VERSION,
    _get_sdk_version,
    _build_sdk_metrics,
)

AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")


class Config:
    cache = None

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @staticmethod
    def get():
        """Raises SkipTest if credentials aren't set up correctly"""
        if Config.cache:
            return Config.cache

        warnings.simplefilter('ignore', ResourceWarning)

        try:
            secrets = boto3.client('secretsmanager', region_name=AWS_DEFAULT_REGION)
            response = secrets.get_secret_value(SecretId='unit-test/endpoint')
            endpoint = response['SecretString']
            Config.cache = Config(endpoint)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as ex:
            print(ex)
            raise unittest.SkipTest("No credentials")

        return Config.cache


def create_client_id():
    return 'test-aws-iot-device-sdk-python-v2-unit-test-{0}'.format(uuid.uuid4())

class TestGetSdkVersion(unittest.TestCase):

    def test_calls_importlib_metadata(self):
        with patch("importlib.metadata.version") as mock_version:
            mock_version.return_value = "1.2.3"
            result = _get_sdk_version()
            mock_version.assert_called_once_with("awsiotsdk")
            self.assertEqual(result, "1.2.3")

    def test_fallback_on_package_not_found(self):
        import importlib.metadata
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = importlib.metadata.PackageNotFoundError("not found")
            result = _get_sdk_version()
            self.assertEqual(result, "dev")

    def test_fallback_on_general_exception(self):
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("unexpected")
            result = _get_sdk_version()
            self.assertEqual(result, "dev")


class TestBuildSdkMetrics(unittest.TestCase):

    def test_library_name(self):
        metrics = _build_sdk_metrics()
        self.assertEqual(metrics.library_name, "IoTDeviceSDK/Python")

    def test_contains_sdk_version(self):
        with patch("awsiot._iot_metrics._get_sdk_version", return_value="1.2.3"):
            metrics = _build_sdk_metrics()
            entries = {e.key: e.value for e in metrics.metadata_entries}
            self.assertIn("IoTSDKVersion", entries)
            self.assertEqual(entries["IoTSDKVersion"], "1.2.3")

    def test_contains_metrics_version(self):
        metrics = _build_sdk_metrics()
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertIn("IoTSDKMetricsVersion", entries)
        self.assertEqual(entries["IoTSDKMetricsVersion"], str(_IOT_SDK_METRICS_VERSION))

    def test_only_two_metadata_entries(self):
        metrics = _build_sdk_metrics()
        self.assertEqual(len(metrics.metadata_entries), 2)

    def test_with_dev_fallback_version(self):
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("no package")
            metrics = _build_sdk_metrics()
            entries = {e.key: e.value for e in metrics.metadata_entries}
            self.assertEqual(entries["IoTSDKVersion"], "dev")


class TestMqtt3BuilderMetrics(unittest.TestCase):
    """Test that mqtt_connection_builder with SDK metrics."""

    def test_metrics_attached(self):
        """Builder should always pass SDK metrics to Connection."""
        config = Config.get()

        with patch("awsiot._iot_metrics._get_sdk_version", return_value="2.0.0"), \
             patch.object(awscrt.mqtt, "Connection") as mock_conn, \
             patch.object(awscrt.mqtt, "Client"):
            mqtt_connection_builder._builder(
                awscrt.io.TlsContextOptions(),
                endpoint=config.endpoint,
                client_id=create_client_id(),
            )

            kwargs = mock_conn.call_args.kwargs
            self.assertIsNotNone(kwargs["metrics"])
            entries = {e.key: e.value for e in kwargs["metrics"].metadata_entries}
            self.assertEqual(entries["IoTSDKVersion"], "2.0.0")
            self.assertEqual(entries["IoTSDKMetricsVersion"], str(_IOT_SDK_METRICS_VERSION))

    def test_metrics_disabled_when_flag_false(self):
        """Builder should suppress SDK metrics when enable_metrics_collection=False."""
        config = Config.get()

        with patch.object(awscrt.mqtt, "Connection") as mock_conn, \
             patch.object(awscrt.mqtt, "Client"):
            mqtt_connection_builder._builder(
                awscrt.io.TlsContextOptions(),
                endpoint=config.endpoint,
                client_id=create_client_id(),
                enable_metrics_collection=False,
            )

            kwargs = mock_conn.call_args.kwargs
            self.assertIsNone(kwargs["metrics"])
            self.assertTrue(kwargs["disable_metrics"])


class TestMqtt5BuilderMetrics(unittest.TestCase):
    """Test that mqtt5_client_builder attaches SDK metrics."""

    def test_metrics_attached(self):
        """Builder should  set SDK metrics on client_options."""
        config = Config.get()

        with patch("awsiot._iot_metrics._get_sdk_version", return_value="2.0.0"), \
             patch.object(awscrt.mqtt5, "Client") as mock_client:
            mqtt5_client_builder._builder(
                awscrt.io.TlsContextOptions(),
                endpoint=config.endpoint,
            )

            client_options = mock_client.call_args.kwargs["client_options"]
            self.assertIsNotNone(client_options.metrics)
            entries = {e.key: e.value for e in client_options.metrics.metadata_entries}
            self.assertEqual(entries["IoTSDKVersion"], "2.0.0")
            self.assertEqual(entries["IoTSDKMetricsVersion"], str(_IOT_SDK_METRICS_VERSION))

    def test_metrics_disabled_when_flag_false(self):
        """Builder should suppress SDK metrics when enable_metrics_collection=False."""
        config = Config.get()

        with patch.object(awscrt.mqtt5, "Client") as mock_client:
            mqtt5_client_builder._builder(
                awscrt.io.TlsContextOptions(),
                endpoint=config.endpoint,
                enable_metrics_collection=False,
            )

            client_options = mock_client.call_args.kwargs["client_options"]
            self.assertTrue(client_options.disable_metrics)


if __name__ == "__main__":
    unittest.main()
