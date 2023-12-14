# AWS IoT Device SDK v2 for Python

[![Version](https://img.shields.io/pypi/v/awsiotsdk.svg?style=flat)](https://pypi.org/project/awsiotsdk/)

This document provides information about the AWS IoT Device SDK v2 for Python. This SDK is built on the [AWS Common Runtime](https://docs.aws.amazon.com/sdkref/latest/guide/common-runtime.html)

*__Jump To:__*
* [Installation](#installation)
* [Samples](samples)
* [Getting Help](#getting-help)
* [FAQ](./documents/FAQ.md)
* [API Docs](https://aws.github.io/aws-iot-device-sdk-python-v2/)
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

# 3. (Optional) Setup the version number of your local build. The default version 
#    for awsiotsdk is set to "1.0.0-dev", you can set the version number of the
#    local build in "aws-iot-device-sdk-python-v2/awsiot/__init__.py"
sed -i "s/__version__ = '1.0.0-dev'/__version__ = '<SDK_VERSION>'/" \
  aws-iot-device-sdk-python-v2/awsiot/__init__.py

# 4. Install using Pip (use 'python' instead of 'python3' on Windows)
python3 -m pip install ./aws-iot-device-sdk-python-v2
```

## Samples

[Samples README](samples)

## Getting Help

The best way to interact with our team is through GitHub. You can open a [discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions) for guidance questions or an [issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues/new/choose) for bug reports, or feature requests. You may also find help on community resources such as [StackOverFlow](https://stackoverflow.com/questions/tagged/aws-iot) with the tag [#aws-iot](https://stackoverflow.com/questions/tagged/aws-iot) or if you have a support plan with [AWS Support](https://aws.amazon.com/premiumsupport/), you can also create a new support case.

Please make sure to check out our resources too before opening an issue:

* [FAQ](./documents/FAQ.md)
* [API Docs](https://aws.github.io/aws-iot-device-sdk-python-v2/)
* [IoT Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) ([source](https://github.com/awsdocs/aws-iot-docs))
* Check for similar [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)
* [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
* [Dev Blog](https://aws.amazon.com/blogs/?awsf.blog-master-iot=category-internet-of-things%23amazon-freertos%7Ccategory-internet-of-things%23aws-greengrass%7Ccategory-internet-of-things%23aws-iot-analytics%7Ccategory-internet-of-things%23aws-iot-button%7Ccategory-internet-of-things%23aws-iot-device-defender%7Ccategory-internet-of-things%23aws-iot-device-management%7Ccategory-internet-of-things%23aws-iot-platform)
* Integration with AWS IoT Services such as
[Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
and [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)
is provided by code that been generated from a model of the service.
* [Contributions Guidelines](./documents/CONTRIBUTING.md)

## License

This library is licensed under the [Apache 2.0 License](./documents/LICENSE).

Latest released version: v1.20.0
