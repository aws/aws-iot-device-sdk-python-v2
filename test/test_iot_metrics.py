# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import unittest

from awsiot._iot_metrics import (
    _SDK_LIBRARY_NAME,
    _IOT_SDK_METRICS_VERSION,
    _get_sdk_version,
    _build_sdk_metrics,
)


class TestGetSdkVersion(unittest.TestCase):

    def test_returns_string(self):
        version = _get_sdk_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


class TestBuildSdkMetrics(unittest.TestCase):

    def test_library_name(self):
        metrics = _build_sdk_metrics()
        self.assertEqual(metrics.library_name, _SDK_LIBRARY_NAME)

    def test_contains_sdk_version(self):
        metrics = _build_sdk_metrics()
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertIn("IoTSDKVersion", entries)
        self.assertEqual(entries["IoTSDKVersion"], _get_sdk_version())

    def test_contains_metrics_version(self):
        metrics = _build_sdk_metrics()
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertIn("IoTSDKMetricsVersion", entries)
        self.assertEqual(entries["IoTSDKMetricsVersion"], str(_IOT_SDK_METRICS_VERSION))

    def test_only_two_metadata_entries(self):
        metrics = _build_sdk_metrics()
        self.assertEqual(len(metrics.metadata_entries), 2)


if __name__ == "__main__":
    unittest.main()
