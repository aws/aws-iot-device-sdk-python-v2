# AWS IoT SDK for Python v2
This document provides information about the AWS IoT device SDK for Python V2.

If you have any issues or feature requests, please file an issue or pull request.

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
* [Giving Feedback and Contributions](#Giving-Feedback-and-Contributions)
* [More Resources](#More-Resources)



## Installation

### Minimum Requirements
*   Python 3.5+

### Install from PyPI
```
pip install awsiotsdk
```

### Install from source
```
pip install ./aws-iot-device-sdk-python-v2
```

### Installation Issues

`awsiotsdk` depends on [awscrt](https://github.com/awslabs/aws-crt-python), which makes use of C extensions. Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux, Raspbian (python3 only)). If wheels are unavailable for your platform (ex: Raspbian with python2.7), your machine must compile some C libraries. If you encounter issues, install the following and try again:

```
sudo apt-get update
sudo apt-get install cmake
sudo apt-get install libssl-dev
```



## Samples

[Samples README](samples)

## Getting Help

Use the following sources for information :

*   Check api and developer guides.
*   Check for similar issues already opened.

If you still can’t find a solution to your problem open an [issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)

## Giving Feedback and Contributions

We need your help in making this SDK great. Please participate in the community and contribute to this effort by submitting issues, participating in discussion forums and submitting pull requests through the following channels.

*   [Contributions Guidelines](master/CONTRIBUTING.md)
*   Articulate your feature request or upvote existing ones on our [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues?q=is%3Aissue+is%3Aopen+label%3Afeature-request) page.
*   Submit [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)



## More Resources

*   [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
*   [Developer Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) ([source](https://github.com/awsdocs/aws-iot-docs))
*   [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)
*   [Dev Blog](https://aws.amazon.com/blogs/?awsf.blog-master-iot=category-internet-of-things%23amazon-freertos%7Ccategory-internet-of-things%23aws-greengrass%7Ccategory-internet-of-things%23aws-iot-analytics%7Ccategory-internet-of-things%23aws-iot-button%7Ccategory-internet-of-things%23aws-iot-device-defender%7Ccategory-internet-of-things%23aws-iot-device-management%7Ccategory-internet-of-things%23aws-iot-platform)

Integration with AWS IoT Services such as
[Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
and [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)
is provided by code that been generated from a model of the service.


# License

This library is licensed under the Apache 2.0 License.
