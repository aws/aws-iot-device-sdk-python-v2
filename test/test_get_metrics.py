# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import unittest
from unittest.mock import patch


class TestImportlibMetadata(unittest.TestCase):
    """Test that importlib.metadata is used instead of pkg_resources"""

    def setUp(self):
        """Reset the metrics string cache before each test"""
        # Reset the cached metrics string in both modules
        import awsiot.mqtt5_client_builder
        import awsiot.mqtt_connection_builder

        # Reset the global _metrics_str variable
        awsiot.mqtt_connection_builder._metrics_str = None
        awsiot.mqtt5_client_builder._metrics_str = None

    def test_metrics_string_generation_mqtt_connection_builder(self):
        """Test that mqtt_connection_builder uses importlib.metadata for version detection"""
        from awsiot import mqtt_connection_builder

        # Mock importlib.metadata.version to return a known version
        with patch("importlib.metadata.version") as mock_version:
            mock_version.return_value = "1.2.3"

            # Call the function that uses version detection
            # We need to access the private function for testing
            result = mqtt_connection_builder._get_metrics_str("test_username")

            # Verify that importlib.metadata.version was called
            mock_version.assert_called_once_with("awsiotsdk")

            # Verify the result contains the expected format
            self.assertIn("SDK=PythonV2&Version=1.2.3", result)

    def test_metrics_string_generation_mqtt5_client_builder(self):
        """Test that mqtt5_client_builder uses importlib.metadata for version detection"""
        from awsiot import mqtt5_client_builder

        # Mock importlib.metadata.version to return a known version
        with patch("importlib.metadata.version") as mock_version:
            mock_version.return_value = "1.2.3"

            # Call the function that uses version detection
            # We need to access the private function for testing
            result = mqtt5_client_builder._get_metrics_str("test_username")

            # Verify that importlib.metadata.version was called
            mock_version.assert_called_once_with("awsiotsdk")

            # Verify the result contains the expected format
            self.assertIn("SDK=PythonV2&Version=1.2.3", result)

    def test_package_not_found_handling_mqtt_connection_builder(self):
        """Test that PackageNotFoundError is handled correctly in mqtt_connection_builder"""
        import importlib.metadata

        from awsiot import mqtt_connection_builder

        # Mock importlib.metadata.version to raise PackageNotFoundError
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = importlib.metadata.PackageNotFoundError("Package not found")

            # Call the function that uses version detection
            result = mqtt_connection_builder._get_metrics_str("test_username")

            # Verify that the fallback version is used
            self.assertIn("SDK=PythonV2&Version=dev", result)

    def test_package_not_found_handling_mqtt5_client_builder(self):
        """Test that PackageNotFoundError is handled correctly in mqtt5_client_builder"""
        import importlib.metadata

        from awsiot import mqtt5_client_builder

        # Mock importlib.metadata.version to raise PackageNotFoundError
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = importlib.metadata.PackageNotFoundError("Package not found")

            # Call the function that uses version detection
            result = mqtt5_client_builder._get_metrics_str("test_username")

            # Verify that the fallback version is used
            self.assertIn("SDK=PythonV2&Version=dev", result)

    def test_general_exception_handling_mqtt_connection_builder(self):
        """Test that general exceptions are handled correctly in mqtt_connection_builder"""
        from awsiot import mqtt_connection_builder

        # Mock importlib.metadata.version to raise a general exception
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("Some other error")

            # Call the function that uses version detection
            result = mqtt_connection_builder._get_metrics_str("test_username")

            # Verify that empty string is returned on general exception
            self.assertEqual(result, "")

    def test_general_exception_handling_mqtt5_client_builder(self):
        """Test that general exceptions are handled correctly in mqtt5_client_builder"""
        from awsiot import mqtt5_client_builder

        # Mock importlib.metadata.version to raise a general exception
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("Some other error")

            # Call the function that uses version detection
            result = mqtt5_client_builder._get_metrics_str("test_username")

            # Verify that empty string is returned on general exception
            self.assertEqual(result, "")

    def test_no_pkg_resources_import(self):
        """Test that pkg_resources is not imported in the modified files"""
        import awsiot.mqtt5_client_builder
        import awsiot.mqtt_connection_builder

        # Check that pkg_resources is not in the module's globals
        self.assertNotIn("pkg_resources", awsiot.mqtt_connection_builder.__dict__)
        self.assertNotIn("pkg_resources", awsiot.mqtt5_client_builder.__dict__)


if __name__ == "__main__":
    unittest.main()
