# AWS IoT Device SDK v2 for Python

[![Version](https://img.shields.io/pypi/v/awsiotsdk.svg?style=flat)](https://pypi.org/project/awsiotsdk/)

This document provides information about the AWS IoT Device SDK v2 for Python.

If you have any issues or feature requests, please file an issue or pull request.

API documentation: https://aws.github.io/aws-iot-device-sdk-python-v2/

This SDK is built on the AWS Common Runtime, a collection of libraries
([aws-c-common](https://github.com/awslabs/aws-c-common),
[aws-c-io](https://github.com/awslabs/aws-c-io),
[aws-c-mqtt](https://github.com/awslabs/aws-c-mqtt),
[aws-c-compression](https://github.com/awslabs/aws-c-compression),
[aws-c-http](https://github.com/awslabs/aws-c-http),
[aws-c-cal](https://github.com/awslabs/aws-c-cal),
[aws-c-auth](https://github.com/awslabs/aws-c-auth),
[s2n](https://github.com/awslabs/s2n) ...) written in C to be
cross-platform, high-performance, secure, and reliable. The libraries are bound
to Python by the `awscrt` package ([PyPI](https://pypi.org/project/awscrt/)) ([Github](https://github.com/awslabs/aws-crt-python)).

*__Jump To:__*
* [Installation](#Installation)
* [Samples](samples)
* [Getting Help](#Getting-Help)
* [FAQ](./documents/FAQ.md)
* [Giving Feedback and Contributions](#Giving-Feedback-and-Contributions)
* [MQTT5 User Guide](./documents/MQTT5_Userguide.md)


## Installation

### Minimum Requirements
* Python 3.7+

[Step-by-step instructions](./documents/PREREQUISITES.md)

### Install from PyPI

#### MacOS and Linux:

```
python3 -m pip install awsiotsdk
```

#### Windows:

```
python -m pip install awsiotsdk
```

### Install from source

```bash
# 1. Create a workspace directory to hold all the SDK files
mkdir sdk-workspace
cd sdk-workspace

# 2. Clone the repository. You could select the version of the SDK you desire to use.
git clone -b <SDK_VERSION> https://github.com/aws/aws-iot-device-sdk-python-v2.git

# 3. (Optional) Setup the version number of your local build. The default version for awsiotsdk is set to "1.0.0-dev", you can set the version number of the local build in "aws-iot-device-sdk-python-v2/awsiot/__init__.py"
sed -i "s/__version__ = '1.0.0-dev'/__version__ = '<SDK_VERSION>'/" aws-iot-device-sdk-python-v2/awsiot/__init__.py

# 4. Install using Pip (use 'python' instead of 'python3' on Windows)
python3 -m pip install ./aws-iot-device-sdk-python-v2
```


### Installation Issues

`awsiotsdk` depends on [awscrt](https://github.com/awslabs/aws-crt-python), which makes use of C extensions. Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux, Raspberry Pi OS). If wheels are unavailable for your platform, your machine must compile some C libraries. For example:

```bash
# 1. Create a workspace directory to hold all the CRT files
mkdir crt-workspace
cd crt-workspace

# 2. Clone the repository, you could select the version you would like to use. You can find the awscrt version used by the current SDK from the file "./aws-iot-device-sdk-python-v2/setup.py". Update the version number in "./aws-iot-device-sdk-python-v2/setup.py" can change the awscrt version you would like to use in awsiotsdk
git clone -b <CRT_VERSION> https://github.com/awslabs/aws-crt-python.git

# 3. Update the submodules
cd aws-crt-python
git submodule update --init --recursive

# 4. (Optional) Setup the version number of your local build. Similar to the awsiotsdk, the default version for awscrt is set to "1.0.0-dev", you can set the version number of the local build in "./aws-crt-python/awscrt/__init__.py". The awscrt version set here need to match the version specified in "./aws-iot-device-sdk-python-v2/setup.py" so that the awsiotsdk could locate the correct awscrt library.
sed -i "s/__version__ = '1.0.0.dev0'/__version__ = '<CRT_VERSION>'/" awscrt/__init__.py

# 5. Install using Pip
python3 -m pip install .
```
If you need aws-crt-python to use the libcrypto included on your system, set environment variable AWS_CRT_BUILD_USE_SYSTEM_LIBCRYPTO=1 while building from source:
```
AWS_CRT_BUILD_USE_SYSTEM_LIBCRYPTO=1 python3 -m pip install --no-binary :all: --verbose awscrt
```
( --no-binary :all: ensures you do not use the precompiled wheel from PyPI)

If you encounter issues, see [Installation Issues](./documents/PREREQUISITES.md#installation-issues) and try again.

## Samples

[Samples README](samples)

## Getting Help

The best way to interact with our team is through GitHub. You can [open an issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues) and choose from one of our templates for guidance, bug reports, or feature requests. You may also find help on community resources such as [StackOverFlow](https://stackoverflow.com/questions/tagged/aws-iot) with the tag #aws-iot or If you have a support plan with [AWS Support](https://aws.amazon.com/premiumsupport/), you can also create a new support case.

Please make sure to check out our resources too before opening an issue:

* Our [FAQ](./documents/FAQ.md)
* [API documentation](https://aws.github.io/aws-iot-device-sdk-python-v2/)
* Our [Developer Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) ([source](https://github.com/awsdocs/aws-iot-docs))
* Check for similar [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)
* [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
* [Dev Blog](https://aws.amazon.com/blogs/?awsf.blog-master-iot=category-internet-of-things%23amazon-freertos%7Ccategory-internet-of-things%23aws-greengrass%7Ccategory-internet-of-things%23aws-iot-analytics%7Ccategory-internet-of-things%23aws-iot-button%7Ccategory-internet-of-things%23aws-iot-device-defender%7Ccategory-internet-of-things%23aws-iot-device-management%7Ccategory-internet-of-things%23aws-iot-platform)
* Integration with AWS IoT Services such as
[Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
and [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)
is provided by code that been generated from a model of the service.

## Giving Feedback and Contributions

We need your help in making this SDK great. Please participate in the community and contribute to this effort by submitting issues, participating in discussion forums and submitting pull requests through the following channels.

* [Contributions Guidelines](./documents/CONTRIBUTING.md)
* Articulate your feature request or upvote existing ones on our [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues?q=is%3Aissue+is%3Aopen+label%3Afeature-request) page.
* Create discussion questions [here](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions)
* Find a bug open an [issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)

## License

This library is licensed under the [Apache 2.0 License](./documents/LICENSE).

Latest released version: v1.17.0
