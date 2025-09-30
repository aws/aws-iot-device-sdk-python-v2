# MQTT5 X509 PubSub

[**Return to main sample list**](../README.md)
*__Jump To:__*
* [Introduction](#introduction)
* [Requirements](#requirements)
* [How To Run](#how-to-run)
* [Additional Information](#additional-information)

## Introduction
This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages through an MQTT connection using MQTT5. 

You can read more about MQTT5 for the Python IoT Device SDK V2 in the [MQTT5 user guide](../../documents/MQTT5_Userguide.md).

## Requirements

This sample assumes you have the required AWS IoT resources available. Information about AWS IoT can be found [HERE](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) and instructions on creating AWS IoT resources (AWS IoT Policy, Device Certificate, Private Key) can be found [HERE](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html).

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:client/mqtt5-sample-*"
      ]
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `mqtt5-sample-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

To Run this sample from the `samples\mqtt` folder, use the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_x509.py \
  --endpoint <AWS IoT endpoint> \
  --cert <Path to certificate file> \
  --key <Path to private key file>
```
If you would like to see what optional arguments are available, use the `--help` argument:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_x509.py --help
```

will result in the following output:
```
MQTT5 X509 Sample (mTLS)

options:
  -h, --help    show this help message and exit

required arguments:
  --endpoint    IoT endpoint hostname (default: None)
  --cert        Path to the certificate file to use during mTLS connection establishment (default: None)
  --key         Path to the private key file to use during mTLS connection establishment (default: None)

optional arguments:
  --client_id   Client ID (default: mqtt5-sample-<uuid>)
  --topic       Topic (default: test/topic)
  --message     Message payload (default: Hello from mqtt5 sample)
  --count       Messages to publish (0 = infinite) (default: 5)
```

The sample will not run without the required arguments and will notify you of missing arguments.

## Additional Information
Additional help with the MQTT5 Client can be found in the [MQTT5 Userguide](../../documents/MQTT5_Userguide.md). This guide will provide more details on MQTT5 [operations](../../documents/MQTT5_Userguide.md#optional-keyword-arguments), [lifecycle events](../../documents/MQTT5_Userguide.md#lifecycle-events), [connection methods](../../documents/MQTT5_Userguide.md#connecting-to-aws-iot-core), and other useful information.

## ⚠️ Usage disclaimer

These code examples interact with services that may incur charges to your AWS account. For more information, see [AWS Pricing](https://aws.amazon.com/pricing/).

Additionally, example code might theoretically modify or delete existing AWS resources. As a matter of due diligence, do the following:

- Be aware of the resources that these examples create or delete.
- Be aware of the costs that might be charged to your account as a result.
- Back up your important data.
