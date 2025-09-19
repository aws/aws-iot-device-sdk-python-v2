# AWS IoT Device SDK for Python v2

[![Version](https://img.shields.io/pypi/v/awsiotsdk.svg?style=flat)](https://pypi.org/project/awsiotsdk/)

The AWS IoT Device SDK for Python v2 connects your Python applications and devices to AWS IoT. Built on the AWS Common Runtime, it handles the complexities of secure communication, authentication, and device management so you can focus on your IoT solution. The SDK makes it easy to use AWS IoT services like Device Shadows, Jobs, and Fleet Provisioning.

**Supported Platforms**: Linux, Windows, macOS

*__Topics:__*
* [Features](#features)
* [Using SDK](#using-sdk)
* [Getting Started](#getting-started)
* [Samples](samples)
* [MQTT5 User Guide](./documents/MQTT5_Userguide.md)
* [Getting Help](#getting-help)
* [Resources](#resources)

## Features

The primary purpose of the AWS IoT Device SDK for Python v2 is to simplify the process of connecting devices to AWS IoT Core and interacting with AWS IoT services on various platforms. The SDK provides:

* Built on the [AWS Common Runtime](https://docs.aws.amazon.com/sdkref/latest/guide/common-runtime.html) for high performance and minimal footprint
* Secure device connections to AWS IoT Core using MQTT protocol including MQTT 5.0
* Support for [multiple authentication methods and connection types](./documents/MQTT5_Userguide.md#how-to-create-an-mqtt5-client-based-on-desired-connection-method)
* First-class support for AWS IoT Core services

#### Supported AWS IoT Core services

* The [AWS IoT Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) service adds shadows to AWS IoT thing objects.
* The [AWS IoT Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) allows to define a set of remote operations that can be sent to and run on one or more devices connected to AWS IoT.
* The [AWS IoT fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html) can generate and securely deliver device certificates and private keys to IoT devices when they connect to AWS IoT for the first time.

## Using SDK

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

```bash
# 1. Create a workspace directory to hold all the SDK files
mkdir sdk-workspace
cd sdk-workspace

# 2. Clone the repository. You could select the version of the SDK you desire to use.
git clone -b <SDK_VERSION> https://github.com/aws/aws-iot-device-sdk-python-v2.git

# 3. (Optional) Setup the version number of your local build. The default version
#    for awsiotsdk is set to "1.0.0-dev", you can set the version number of the
#    local build in "aws-iot-device-sdk-python-v2/awsiot/__init__.py"
sed -i "s/__version__ = '1.0.0-dev'/__version__ = '<SDK_VERSION>'/" \
  aws-iot-device-sdk-python-v2/awsiot/__init__.py

# 4. Install using Pip (use 'python' instead of 'python3' on Windows)
python3 -m pip install ./aws-iot-device-sdk-python-v2
```

## Getting Started

To get started with the AWS IoT Device SDK for Python v2:

1. **Install the SDK** - See the [Using SDK](#using-sdk) section for installation details

2. **Choose your connection method** - The SDK supports multiple authentication methods including X.509 certificates, AWS credentials, and custom authentication

3. **Follow a complete example** - Check out the [samples](samples) directory for working code examples that demonstrate:
   - Basic MQTT connection and messaging
   - Device Shadow operations
   - AWS IoT Jobs
   - Fleet provisioning

4. **Learn MQTT5 features** - For advanced usage and configuration options, see the [MQTT5 User Guide](./documents/MQTT5_Userguide.md)

The samples provide ready-to-run code with detailed setup instructions for each authentication method and use case.

## Samples

Check out the [samples](samples) directory for working code examples that demonstrate:
- Basic MQTT connection and messaging
- AWS IoT Device Shadow operations
- AWS IoT Jobs
- AWS IoT Fleet provisioning

The samples provide ready-to-run code with detailed setup instructions for each authentication method and use case.

## Getting Help

The best way to interact with our team is through GitHub.
* Open [discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions): Share ideas and solutions with the SDK community
* Search [issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues): Find created issues for answers based on a topic
* Create an [issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues/new/choose): New feature request or file a bug

If you have a support plan with [AWS Support](https://aws.amazon.com/premiumsupport/), you can also create a new support case.

#### Mac-Only TLS Behavior

Please note that on Mac, once a private key is used with a certificate, that certificate-key pair is imported into the Mac Keychain.  All subsequent uses of that certificate will use the stored private key and ignore anything passed in programmatically.  Beginning in v1.7.3, when a stored private key from the Keychain is used, the following will be logged at the "info" log level:

```
static: certificate has an existing certificate-key pair that was previously imported into the Keychain.  Using key from Keychain instead of the one provided.
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

Latest released version: v1.24.0
