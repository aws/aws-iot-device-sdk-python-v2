# MQTT5 Custom Authorizer PubSub

[**Return to main sample list**](../README.md)
*__Jump To:__*
* [Introduction](#introduction)
* [Requirements](#requirements)
* [How To Run](#how-to-run)
* [Additional Information](#additional-information)

## Introduction
The Custom Authorizer samples illustrate how to connect to the [AWS IoT Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html) with the MQTT5 Client by authenticating with a signed or unsigned [Custom Authorizer Lambda Function](https://docs.aws.amazon.com/iot/latest/developerguide/custom-auth-tutorial.html)

You can read more about MQTT5 for the Python IoT Device SDK V2 in the [MQTT5 user guide](../../documents/MQTT5_Userguide.md).

## Requirements

You will need to setup your Custom Authorizer so the Lambda function returns a policy document. See [this page on the documentation](https://docs.aws.amazon.com/iot/latest/developerguide/config-custom-auth.html) for more details and example return result. You can customize this lambda function as needed for your application to provide your own security measures based on the needs of your application.

The policy [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) provided by your Custom Authorizer Lambda must provide iot connect, subscribe, publish, and receive privileges for this sample to run successfully.

Below is a sample policy that provides the necessary privileges.

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

# For an unsigned custom authorizer
python3 mqtt5_custom_auth_unsigned.py \
    --endpoint <AWS IoT endpoint> \
    --authorizer_name <The name of the custom authorizer to invoke> \
    --auth_username <The name to send when connecting through the custom authorizer>\
    --auth_password <The password to send when connecting through a custom authorizer>

# For a signed custom authorizer
python3 mqtt5_custom_auth_signed.py \
    --endpoint <AWS IoT endpoint> \
    --authorizer_name <The name of the custom authorizer to invoke> \
    --auth_token_key_name <Authorizer token key name> \
    --auth_token_key_value <Authorizer token key value> \
    --auth_signature <Custom authorizer signature> \
    --auth_username <The name to send when connecting through the custom authorizer> \
    --auth_password <The password to send when connecting through a custom authorizer>

```
If you would like to see optional arguments, use the `--help` argument:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'

# For an unsigned custom authorizer
python3 mqtt5_custom_auth_unsigned.py --help

# For a signed custom authorizer
python3 mqtt5_custom_auth_signed.py --help
```

will result in the following output:
```
MQTT5 Unsigned Custom Authorizer Sample

options:
  -h, --help            show this help message and exit

required arguments:
  --endpoint            IoT endpoint hostname (default: None)
  --authorizer_name     The name of the custom authorizer to connect to invoke (default: None)
  --auth_signature      Custom authorizer signature (default: None)
  --auth_token_key_name 
                        Authorizer token key name (default: None)
  --auth_token_key_value 
                        Authorizer token key value (default: None)
  --auth_username       The name to send when connecting through the custom authorizer (optional) (default: None)
  --auth_password       The password to send when connecting through a custom authorizer (optional) (default: None)

optional arguments:
  --client_id           Client ID (default: mqtt5-sample-<uuid>)
  --topic               Topic (default: test/topic)
  --message             Message payload (default: Hello from mqtt5 sample)
  --count               Messages to publish (0 = infinite) (default: 5)
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
