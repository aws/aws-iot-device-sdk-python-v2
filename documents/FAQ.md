# Frequently Asked Questions

### Where should I start?

If you are just getting started make sure you [install this sdk](https://github.com/aws/aws-iot-device-sdk-python-v2#installation) and then build and run the [basic PubSub](https://github.com/aws/aws-iot-device-sdk-python-v2/tree/main/samples#pubsub)

### How do I enable logging?

``` python
io.init_logging(io.LogLevel.Error, 'stderr')
```
You can also enable [CloudWatch logging](https://docs.aws.amazon.com/iot/latest/developerguide/cloud-watch-logs.html) for IoT which will provide you with additional information that is not available on the client side sdk.

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

### Mac-Only TLS Behavior

Please note that on Mac, once a private key is used with a certificate, that certificate-key pair is imported into the Mac Keychain.  All subsequent uses of that certificate will use the stored private key and ignore anything passed in programmatically.  Beginning in v1.7.3, when a stored private key from the Keychain is used, the following will be logged at the "info" log level:

```
static: certificate has an existing certificate-key pair that was previously imported into the Keychain.  Using key from Keychain instead of the one provided.
```

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
            "program": "${workspaceFolder}/samples/pubsub.py",
            "args": [
                "--endpoint", "<account-number>-ats.iot.<region>.amazonaws.com",
                "--ca_file", "<path to root-CA>",
                "--cert", "<path to cert>",
                "--key", "<path to key>",
                "--client-id", "test-client"
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

### I still have more questions about the this sdk?

* [Here](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) are the AWS IoT Core docs for more details about IoT Core
* [Here](https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html) are the AWS IoT Greengrass v2 docs for more details about greengrass
* [Discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions) questions are also a great way to ask other questions about this sdk.
* [Open an issue](https://github.com/aws/aws-iot-device-sdk-python-v2/issues) if you find a bug or have a feature request
