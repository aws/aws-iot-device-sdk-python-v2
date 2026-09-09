# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

"""
Private IoT SDK metrics module.

Provides SDK-level metadata (version info) to pass to the CRT layer.
The CRT handles all feature detection (certificate source, TLS settings, etc.)
and embeds the combined metrics in the MQTT CONNECT packet username field.

"""

from awscrt.aws_iot_metrics import AWSIoTMetrics, IoTMetricsMetadata

# The current version of the IoT SDK metrics format.
# This must match the version expected by CRT layer.
_IOT_SDK_METRICS_VERSION = 1


def _get_sdk_version():
    """
    Return the installed ``awsiotsdk`` package version string.

    Falls back to ``"dev"`` if the package metadata is unavailable (e.g. when
    running from a source checkout without installing).

    Returns:
        str: A version string like ``1.32.0`` or ``"dev"``.
    """
    try:
        import importlib.metadata
        return importlib.metadata.version("awsiotsdk")
    except Exception:
        return "dev"


def _build_sdk_metrics():
    """
    Build the SDK-level :class:`~awscrt.aws_iot_metrics.AWSIoTMetrics` payload
    that is passed down to the CRT layer.

    The returned object carries SDK identity and the metrics format version
    via two metadata entries:

    - ``IoTSDKVersion``: the installed ``awsiotsdk`` package version, used
      to identify the SDK release on the server side.
    - ``IoTSDKMetricsVersion``: the metrics format version this SDK supports.
      The CRT only merges SDK-supplied features when this value matches the
      version it expects, so bumping :data:`_IOT_SDK_METRICS_VERSION` should
      be done in lockstep with CRT changes.

    The CRT layer is responsible for detecting connection-level features
    (protocol version, certificate source, TLS settings, proxy type, etc.)
    and appending them to the metadata before embedding the result in the
    MQTT CONNECT packet username field.

    Returns:
        AWSIoTMetrics: A populated metrics object ready to attach to an
        MQTT5 client or MQTT3 connection configuration.
    """
    return AWSIoTMetrics(
        metadata_entries=[
            IoTMetricsMetadata(key="IoTSDKVersion", value=_get_sdk_version()),
            IoTMetricsMetadata(key="IoTSDKMetricsVersion", value=str(_IOT_SDK_METRICS_VERSION)),
        ]
    )
