# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import unittest

from awsiot.iot_metrics import (
    CertificateSource,
    FeatureId,
    SDK_LIBRARY_NAME,
    _encode_feature_list,
    _get_sdk_version,
    build_sdk_metrics,
)


class TestFeatureEncoding(unittest.TestCase):

    def test_certificate_files(self):
        self.assertEqual(_encode_feature_list(CertificateSource.CERTIFICATE_FILES), "I/A")

    def test_pkcs11(self):
        self.assertEqual(_encode_feature_list(CertificateSource.PKCS11), "I/B")

    def test_windows_cert_store(self):
        self.assertEqual(_encode_feature_list(CertificateSource.WINDOWS_CERT_STORE), "I/C")

    def test_pkcs12(self):
        self.assertEqual(_encode_feature_list(CertificateSource.PKCS12_FILE), "I/E")

    def test_none_returns_empty(self):
        self.assertEqual(_encode_feature_list(None), "")


class TestGetSdkVersion(unittest.TestCase):

    def test_returns_string(self):
        version = _get_sdk_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


class TestBuildSdkMetrics(unittest.TestCase):

    def test_with_certificate_source(self):
        metrics = build_sdk_metrics(CertificateSource.CERTIFICATE_FILES)

        self.assertEqual(metrics.library_name, SDK_LIBRARY_NAME)
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertIn("IoTSDKVersion", entries)
        self.assertEqual(entries["IoTSDKFeature"], "I/A")
        self.assertIn("IoTSDKMetricsVersion", entries)

    def test_without_certificate_source(self):
        metrics = build_sdk_metrics(None)

        self.assertEqual(metrics.library_name, SDK_LIBRARY_NAME)
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertIn("IoTSDKVersion", entries)
        self.assertNotIn("IoTSDKFeature", entries)
        self.assertNotIn("IoTSDKMetricsVersion", entries)

    def test_pkcs11_feature(self):
        metrics = build_sdk_metrics(CertificateSource.PKCS11)
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertEqual(entries["IoTSDKFeature"], "I/B")

    def test_pkcs12_feature(self):
        metrics = build_sdk_metrics(CertificateSource.PKCS12_FILE)
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertEqual(entries["IoTSDKFeature"], "I/E")

    def test_windows_cert_store_feature(self):
        metrics = build_sdk_metrics(CertificateSource.WINDOWS_CERT_STORE)
        entries = {e.key: e.value for e in metrics.metadata_entries}
        self.assertEqual(entries["IoTSDKFeature"], "I/C")

    def test_library_name(self):
        metrics = build_sdk_metrics(CertificateSource.CERTIFICATE_FILES)
        self.assertEqual(metrics.library_name, "IoTDeviceSDK/Python")

    def test_metrics_version_only_set_with_features(self):
        metrics_with = build_sdk_metrics(CertificateSource.CERTIFICATE_FILES)
        metrics_without = build_sdk_metrics(None)

        entries_with = {e.key for e in metrics_with.metadata_entries}
        entries_without = {e.key for e in metrics_without.metadata_entries}

        self.assertIn("IoTSDKMetricsVersion", entries_with)
        self.assertNotIn("IoTSDKMetricsVersion", entries_without)


class TestEnumValues(unittest.TestCase):

    def test_feature_id(self):
        self.assertEqual(FeatureId.CERTIFICATE_SOURCE.value, "I")

    def test_certificate_source_values(self):
        self.assertEqual(CertificateSource.CERTIFICATE_FILES.value, "A")
        self.assertEqual(CertificateSource.PKCS11.value, "B")
        self.assertEqual(CertificateSource.WINDOWS_CERT_STORE.value, "C")
        self.assertEqual(CertificateSource.PKCS12_FILE.value, "E")


if __name__ == "__main__":
    unittest.main()
