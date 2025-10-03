# AWS IoT Device SDK for Python v2

[![Version](https://img.shields.io/pypi/v/awsiotsdk.svg?style=flat)](https://pypi.org/project/awsiotsdk/)

The AWS IoT Device SDK for Python v2 connects your Python applications and devices to the AWS IoT platform. It handles the complexities of secure communication, authentication, and device management so you can focus on your IoT solution. The SDK makes it easy to use AWS IoT services like Device Shadows, Jobs, and Fleet Provisioning.

**Supported Platforms**: Linux, Windows 11+, macOS 14+

> **Note**: The SDK is known to work on older platform versions, but we only guarantee compatibility for the platforms listed above.

*__Topics:__*
* [Features](#features)
* [Installation](#installation)
  * [Minimum Requirements](#minimum-requirements)
  * [Installing from PyPI](#installing-from-pypi)
* [Getting Started](#getting-started)
* [Samples](samples)
* [MQTT5 User Guide](./documents/MQTT5_Userguide.md)
* [Getting Help](#getting-help)
* [Resources](#resources)

## Features

The primary purpose of the AWS IoT Device SDK for Python v2 is to simplify the process of connecting devices to AWS IoT Core and interacting with AWS IoT services on various platforms. The SDK provides:

* Integrated service clients for AWS IoT Core services
* Secure device connections to AWS IoT Core using MQTT protocol including MQTT 5.0
* Support for [multiple authentication methods and connection types](./documents/MQTT5_Userguide.md#how-to-create-an-mqtt5-client-based-on-desired-connection-method)

#### Supported AWS IoT Core services

* The [AWS IoT Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) service manages device state information in the cloud.
* The [AWS IoT Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) service sends remote operations to connected devices.
* The [AWS IoT fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html) service generates and delivers device certificates automatically.

## Installation

The recommended way to use the AWS IoT Device SDK for Python v2 in your project is to install it from PyPI.

### Minimum Requirements

To develop applications with the AWS IoT Device SDK for Python v2, you need:

* Python 3.8+

See [detailed setup instructions](./documents/PREREQUISITES.md) for more information.

### Installing from PyPI

#### macOS and Linux:

```bash
python3 -m pip install awsiotsdk
```

#### Windows:

```bash
python -m pip install awsiotsdk
```

### Building from source

See the [Development Guide](./documents/DEVELOPING.md) for detailed instructions on building from source and using local builds.

## Getting Started

To get started with the AWS IoT Device SDK for Python v2:

1. **Install the SDK** - See the [Installation](#installation) section for installation details

2. **Choose your connection method** - The SDK supports multiple authentication methods including X.509 certificates, AWS credentials, and custom authentication. [MQTT5 User Guide connection section](./documents/MQTT5_Userguide.md#how-to-create-an-mqtt5-client-based-on-desired-connection-method) and [MQTT5 X509 sample](./samples/mqtt/mqtt5_x509.md) provide more guidance

3. **Follow a complete example** - Check out the [samples](samples) directory

4. **Learn MQTT5 features** - For advanced usage and configuration options, see the [MQTT5 User Guide](./documents/MQTT5_Userguide.md)

## Samples

Check out the [samples](samples) directory for working code examples that demonstrate:
- [Basic MQTT connection and messaging](./samples/mqtt/mqtt5_x509.md)
- [AWS IoT Device Shadow operations](./samples/service_clients/shadow.md)
- [AWS IoT Jobs](./samples/service_clients/jobs.md)
- AWS IoT Fleet provisioning: [basic](./samples/service_clients/fleet_provisioning_basic.md) and [with CSR](./samples/service_clients/fleet_provisioning_csr.md)

The samples provide ready-to-run code with detailed setup instructions for each authentication method and use case.

## Getting Help

The best way to interact with our team is through GitHub.
* Open [discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions): Share ideas and solutions with the SDK community
* Search [issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues): Find created issues for answers based on a topic
* Create an [issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues/new/choose): New feature request or file a bug

If you have a support plan with [AWS Support](https://aws.amazon.com/premiumsupport/), you can also create a new support case.

#### Mac-Only TLS Behavior

> [!NOTE]
> This SDK does not support TLS 1.3 on macOS. Support for TLS 1.3 on macOS is planned for a future release.

Please note that on Mac, once a private key is used with a certificate, that certificate-key pair is imported into the Mac Keychain.  All subsequent uses of that certificate will use the stored private key and ignore anything passed in programmatically.  Beginning in v1.7.3, when a stored private key from the Keychain is used, the following will be logged at the "info" log level:

```
static: certificate has an existing certificate-key pair that was previously imported into the Keychain.
 Using key from Keychain instead of the one provided.
```

## Resources

Check out our resources for additional guidance too before opening an issue:

* [FAQ](./documents/FAQ.md)
* [AWS IoT Core Developer Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)
* [MQTT5 User Guide](./documents/MQTT5_Userguide.md)
* [API Docs](https://aws.github.io/aws-iot-device-sdk-python-v2/)
* [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
* [Dev Blog](https://aws.amazon.com/blogs/iot/category/internet-of-things/)
* [Migration Guide from the AWS IoT SDK for Python v1](./documents/MIGRATION_GUIDE.md)
* [Contributions Guidelines](./documents/CONTRIBUTING.md)

## License

This library is licensed under the [Apache 2.0 License](./documents/LICENSE).

Latest released version: v1.26.0
