# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

"""
IoT SDK Metrics V2 - SDK layer feature tracking.

This module implements the SDK-side of the IoT Metrics.
It collects SDK-level feature usage information (such as the certificate source
used for authentication) and packages it into an :class:`~awscrt.aws_iot_metrics.AWSIoTMetrics`
object. The CRT layer then merges these SDK-level features with its own CRT-level
features and embeds the combined metrics string in the MQTT CONNECT packet's
username field.

Metrics Flow:
    1. A connection builder determines which certificate source is in use.
    2. :func:`build_sdk_metrics` is called with the appropriate
       :class:`CertificateSource` value (or ``None`` for connections that
       don't use client certificates, e.g. websocket or custom auth).
    3. The returned :class:`~awscrt.aws_iot_metrics.AWSIoTMetrics` object is
       passed to the CRT connection/client, which handles final encoding into
       the CONNECT username.

Feature Encoding Format:
    SDK features are encoded as comma-separated ``ID/Value`` pairs.
    For example, certificate source PKCS11 is encoded as ``I/B``.
"""

from enum import Enum
from typing import Optional

from awscrt.aws_iot_metrics import AWSIoTMetrics, IoTMetricsMetadata, IOT_SDK_METRICS_FEATURE_VERSION

SDK_LIBRARY_NAME = "IoTDeviceSDK/Python"

class FeatureId(str, Enum):
    """SDK-layer feature identifiers.

    Each member maps a feature name to the single-character ID
    used in the encoded metrics string.

    Attributes:
        CERTIFICATE_SOURCE: Tracks which certificate/authentication method is
            used for the connection. Encoded values come from :class:`CertificateSource`.
    """
    CERTIFICATE_SOURCE = "I"

class CertificateSource(str, Enum):
    """Certificate source identifiers for metrics feature ``I``.

    Each value corresponds to a specific authentication method used by the
    MQTT connection. The single-character value is what gets encoded into the
    metrics string sent in the CONNECT packet.

    Note:
        Value ``"D"`` (Java KeyStore) is reserved for the Java SDK and is not
        applicable to the Python SDK. It is intentionally skipped here.

    Attributes:
        CERTIFICATE_FILES: Client certificate and private key provided as file paths.
        PKCS11: Private key stored in a PKCS#11-compatible hardware security module.
        WINDOWS_CERT_STORE: Certificate retrieved from the Windows system certificate store.
        PKCS12_FILE: Certificate and private key bundled in a PKCS#12 (.p12/.pfx) file.
    """
    CERTIFICATE_FILES = "A"
    PKCS11 = "B"
    WINDOWS_CERT_STORE = "C"
    # "D" is Java KeyStore — not applicable to the Python SDK.
    PKCS12_FILE = "E"



def _get_sdk_version():
    """Return the installed ``awsiotsdk`` package version string.

    Falls back to ``"dev"`` if the package metadata is unavailable (e.g. when
    running from a source checkout without installing).

    Returns:
        str: A version string like ``"1.21.0"`` or ``"dev"``.
    """
    try:
        import importlib.metadata
        return importlib.metadata.version("awsiotsdk")
    except Exception:
        return "dev"


def _encode_feature_list(certificate_source: Optional[CertificateSource] = None) -> str:
    """Encode SDK features into the ``ID/Value,...`` wire format.

    Each feature is represented as its :class:`FeatureId` character followed by
    a slash and the feature-specific value character. Multiple features would be
    separated by commas (currently only one feature is tracked).

    Args:
        certificate_source: The certificate method in use, or ``None`` if no
            client certificate is involved.

    Returns:
        str: Encoded feature string (e.g. ``"I/A"``), or an empty string if no
        features apply.
    """
    if certificate_source is not None:
        return f"{FeatureId.CERTIFICATE_SOURCE.value}/{certificate_source.value}"
    return ""


def build_sdk_metrics(certificate_source: Optional[CertificateSource] = None) -> AWSIoTMetrics:
    """Build an :class:`~awscrt.aws_iot_metrics.AWSIoTMetrics` instance for the CRT layer.

    This is the main entry point for SDK metrics. Connection builders call this
    function to produce the metrics object that the CRT will merge with its own
    metrics and embed in the MQTT CONNECT username.

    The returned object always includes:
        - ``IoTSDKVersion``: The installed SDK version string.

    When a *certificate_source* is provided, it additionally includes:
        - ``IoTSDKFeature``: Encoded feature string (e.g. ``"I/A"``).
        - ``IoTSDKMetricsVersion``: The metrics protocol version supported.

    Args:
        certificate_source: The certificate/authentication method used by this
            connection. Pass ``None`` for connections that don't use client
            certificates (e.g. websocket with SigV4, custom authorizers).

    Returns:
        AWSIoTMetrics: A metrics object ready to be passed to the CRT
        connection or client builder.
    """
    metadata = [
        IoTMetricsMetadata(key="IoTSDKVersion", value=_get_sdk_version()),
    ]

    feature_list = _encode_feature_list(certificate_source)
    if feature_list:
        metadata.append(IoTMetricsMetadata(key="IoTSDKFeature", value=feature_list))
        metadata.append(IoTMetricsMetadata(key="IoTSDKMetricsVersion", value=str(IOT_SDK_METRICS_FEATURE_VERSION)))

    return AWSIoTMetrics(library_name=SDK_LIBRARY_NAME, metadata_entries=metadata)
