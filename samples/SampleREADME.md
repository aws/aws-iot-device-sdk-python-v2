# PubSub Sample

[**Return to main sample list**](./README.md)

This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages through an MQTT connection.

On startup, the device connects to the server, subscribes to a topic, and begins publishing messages to that topic. The device should receive those same messages back from the message broker, since it is subscribed to that same topic. Status updates are continually printed to the console. This sample demonstrates how to send and receive messages on designated IoT Core topics, an essential task that is the backbone of many IoT applications that need to send data over the internet. This sample simply subscribes and publishes to a topic, printing the messages it just sent as it is received from AWS IoT Core, but this can be used as a reference point for more complex Pub-Sub applications.

## Before you run the sample

0. [What is AWS IOT?](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)

1. Setup AWS account and [create AWS IoT Resource](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html): Make sure you download and save the certificate files from the creation.
   
2. Check AWS IoT Policy

   Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

    For the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

   <details>
    <summary>(see sample policy)</summary>
    <pre>
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "iot:Publish",
            "iot:Receive"
          ],
          "Resource": [
            "arn:aws:iot:<b>region</b>:<b>account</b>:topic/test/topic"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "iot:Subscribe"
          ],
          "Resource": [
            "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/test/topic"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "iot:Connect"
          ],
          "Resource": [
            "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
          ]
        }
      ]
    }
    </pre>

    Replace with the following with the data from your AWS account:
    * `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
    * `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.

    Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK.

    </details>

3. [Install the SDK](../README.md#Installation).

## How to run the sample

To Run this sample from the `samples` folder, use the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub.py --endpoint <endpoint> --cert <file> --key <file>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub.py --endpoint <endpoint> --cert <file> --key <file> --ca_file <file>
```

## Trouble Shoot
### Sample Help

All samples will show their options by passing in `--help`. For example:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub.py --help
```

Which will result in output showing all of the options that can be passed in at the command line, along with descriptions of what each does and whether they are optional or not.

### Enable logging in samples

To enable logging in the samples, you need to pass the `--verbosity` as an additional argument. `--verbosity` controls the level of logging shown. `--verbosity` can be set to `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`, or `None`.

For example, to run [MQTT5 PubSub](./mqtt5_pubsub.md) sample with logging you could use the following:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub.py <other arguments> --verbosity Debug
```

### Others
Please make sure to check out our resources too before opening an DISCUSSION:

* [FAQ](./documents/FAQ.md)
* [API Docs](https://aws.github.io/aws-iot-device-sdk-python-v2/)
* [IoT Guide](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)
* Check for similar [Issues](https://github.com/aws/aws-iot-device-sdk-python-v2/issues)
* [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
* [Dev Blog](https://aws.amazon.com/blogs/?awsf.blog-master-iot=category-internet-of-things%23amazon-freertos%7Ccategory-internet-of-things%23aws-greengrass%7Ccategory-internet-of-things%23aws-iot-analytics%7Ccategory-internet-of-things%23aws-iot-button%7Ccategory-internet-of-things%23aws-iot-device-defender%7Ccategory-internet-of-things%23aws-iot-device-management%7Ccategory-internet-of-things%23aws-iot-platform)

