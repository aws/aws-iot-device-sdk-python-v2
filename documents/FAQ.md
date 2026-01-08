# Frequently Asked Questions

*__Jump To:__*
* [Where should I start](#where-should-i-start)
* [How do I enable logging](#how-do-i-enable-logging)
* [How do I get more information from an error code](#how-do-i-get-more-information-from-an-error-code)
* [Installation Issues](#installation-issues)
* [I keep getting AWS_ERROR_MQTT_UNEXPECTED_HANGUP](#i-keep-getting-aws_error_mqtt_unexpected_hangup)
* [I am experiencing deadlocks](#i-am-experiencing-deadlocks)
* [How do debug in VSCode?](#how-do-debug-in-vscode)
* [What certificates do I need?](#what-certificates-do-i-need)
* [Where can I find MQTT 311 Samples?](#where-can-i-find-mqtt-311-samples)
* [I still have more questions about this sdk?](#i-still-have-more-questions-about-this-sdk)

### Where should I start?

If you are just getting started make sure you [install this sdk](https://github.com/aws/aws-iot-device-sdk-python-v2#installation) and then build and run the [basic PubSub](https://github.com/aws/aws-iot-device-sdk-python-v2/tree/main/samples#pubsub)

### How do I enable logging?
To enable logging you must import `io` from `awscrt` and initialize it with `init_logging`.

`LogLevel` can be set to `Fatal`, `Error`, `Warn`, `Info`, `Debug`, or `Trace`. `stderr` and `stdout` can be used to print logs while any other string will be assumed to be a file path. 
``` python
from awscrt import io
# This sets the logger to print any Error level logs to stderr
io.init_logging(io.LogLevel.Error, 'stderr')
```
You can also enable [CloudWatch logging](https://docs.aws.amazon.com/iot/latest/developerguide/cloud-watch-logs.html) for IoT which will provide you with additional information that is not available on the client side sdk.

### How do I get more information from an error code?

When you encounter an `AwsCrtError`, you can get error details using `str()` or `repr()`:

```python
try:
    # Your AWS IoT code here
    pass
except Exception as e:
    print(f"Error: {e}")        # Using str()
    print(f"Error: {repr(e)}")  # Using repr() for more details
```

**Example output:** 
```
# Assume we got error 1059, AWS_IO_DNS_INVALID_NAME
Error: AWS_IO_DNS_INVALID_NAME: Host name was invalid for dns resolution."
Error: AwsCrtError(name='AWS_IO_DNS_INVALID_NAME', message='Host name was invalid for dns resolution.', code=1059)
```

### Installation Issues

`awsiotsdk` depends on [awscrt](https://github.com/awslabs/aws-crt-python), which makes use of C extensions. Precompiled wheels are downloaded when installing on major platforms (Mac, Windows, Linux, Raspberry Pi OS). If wheels are unavailable for your platform, your machine must compile some C libraries. For example:

```bash
# 1. Create a workspace directory to hold all the CRT files
mkdir crt-workspace
cd crt-workspace

# 2. Clone the repository, you could select the version you would like to use. You can find the awscrt 
#    version used by the current SDK from the file "./aws-iot-device-sdk-python-v2/setup.py". Update 
#    the version number in "./aws-iot-device-sdk-python-v2/setup.py" can change the awscrt version 
#    you would like to use in awsiotsdk
git clone -b <CRT_VERSION> https://github.com/awslabs/aws-crt-python.git

# 3. Update the submodules
cd aws-crt-python
git submodule update --init --recursive

# 4. (Optional) Setup the version number of your local build. Similar to the awsiotsdk, the default 
#    version for awscrt is set to "1.0.0-dev", you can set the version number of the local build in 
#    "./aws-crt-python/awscrt/__init__.py". The awscrt version set here need to match the version 
#    specified in "./aws-iot-device-sdk-python-v2/setup.py" so that the awsiotsdk could locate the 
#    correct awscrt library.
sed -i "s/__version__ = '1.0.0.dev0'/__version__ = '<CRT_VERSION>'/" awscrt/__init__.py

# 5. Install using Pip
python3 -m pip install .
```
If you need aws-crt-python to use the libcrypto included on your system, set environment variable AWS_CRT_BUILD_USE_SYSTEM_LIBCRYPTO=1 while building from source:
```
AWS_CRT_BUILD_USE_SYSTEM_LIBCRYPTO=1 python3 -m pip install --no-binary :all: --verbose awscrt
```
( --no-binary :all: ensures you do not use the precompiled wheel from PyPI)

If you encounter issues, see [Installation Issues](./PREREQUISITES.md#installation-issues) and try again.


### I keep getting AWS_ERROR_MQTT_UNEXPECTED_HANGUP

This could be many different things but it most likely is a policy issue. Start with using a super permissive IAM policy called AWSIOTFullAccess which looks like this:

``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iot:*"
            ],
            "Resource": "*"
        }
    ]
}
```

After getting it working make sure to only allow the actions and resources that you need. More info about IoT IAM policies can be found [here](https://docs.aws.amazon.com/iot/latest/developerguide/security_iam_service-with-iam.html).

### I am experiencing deadlocks
You MUST NOT perform blocking operations on any callback, or you will cause a deadlock. For example: in the on_publish_received callback, do not send a publish, and then wait for the future to complete within the callback. The Client cannot do work until your callback returns, so the thread will be stuck.

### How do debug in VSCode?

Here is an example launch.json file to run the pubsub sample
 ``` json
 {
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "PubSub",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/samples/mqtt/mqtt5_x509.py",
            "args": [
                "--endpoint", "<account-number>-ats.iot.<region>.amazonaws.com",
                "--cert", "<path to cert>",
                "--key", "<path to key>",
                "--client_id", "test-client"
            ]
        }
    ]
}
```

### What certificates do I need?

* You can download pre-generated certificates from the AWS console (this is the simplest and is recommended for testing)
* You can also generate your own certificates to fit your specific use case. You can find documentation for that [here](https://docs.aws.amazon.com/iot/latest/developerguide/x509-client-certs.html) and [here](https://iot-device-management.workshop.aws/en/provisioning-options.html)
* Certificates that you will need to run the samples
    * Root CA Certificates
        * Download the root CA certificate file that corresponds to the type of data endpoint and cipher suite you're using (You most likely want Amazon Root CA 1)
        * Generated and provided by Amazon. You can download it [here](https://www.amazontrust.com/repository/) or download it when getting the other certificates from the AWS console
        * When using samples it can look like this: `--ca_file root-CA.crt`
    * Device certificate
        * Intermediate device certificate that is used to generate the key below
        * When using samples it can look like this: `--cert abcde12345-certificate.pem.crt`
    * Key files
        * You should have generated/downloaded private and public keys that will be used to verify that communications are coming from you
        * When using samples you only need the private key and it will look like this: `--key abcde12345-private.pem.key`

### Where can I find MQTT 311 Samples?
The MQTT 311 Samples can be found in the v1.24.0 samples folder [here](https://github.com/aws/aws-iot-device-sdk-python-v2/tree/v1.24.0/samples)

### I still have more questions about this sdk?

* [Here](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) are the AWS IoT Core docs for more details about IoT Core
* [Here](https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html) are the AWS IoT Greengrass v2 docs for more details about greengrass
* [Discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions) questions are also a great way to ask other questions about this sdk.
* [Open an issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues) if you find a bug or have a feature request
