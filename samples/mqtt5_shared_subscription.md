# MQTT5 Shared Subscription

[**Return to main sample list**](./README.md)

This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages over a MQTT5 connection using a shared subscription.

MQTT5 introduces additional features and enhancements that improve the development experience with MQTT. You can read more about MQTT5 in the Python V2 SDK by checking out the [MQTT5 user guide](../documents/MQTT5_Userguide.md).

[Shared Subscriptions](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt5-shared-subscription) allow IoT devices to connect to a group where messages sent to a topic are then relayed to the group in a round-robin-like fashion. This is useful for distributing message load across multiple subscribing MQTT5 clients automatically. This is helpful for load balancing when you have many messages that need to be processed.

Shared Subscriptions rely on a group name/identifier, which tells the MQTT5 broker/server which IoT devices to treat as a group for message distribution. This is done when subscribing by formatting the subscription topic like the following: `$share/<ShareName>/<TopicFilter>`.
* `$share`: Tells the MQTT5 broker/server that the device is subscribing to a Shared Subscription.
* `<ShareName>`: Tells the MQTT5 broker/server which group to add this Shared Subscription to. Messages published to a matching topic will be distributed round-robin amongst the group.
* `<TopicFilter>`: The topic that the Shared Subscription is for. Messages published to this topic will be processed in a round-robin fashion. For example, `test/topic`.

Shared Subscriptions use a round-robbin like method of distributing messages for the subscribed clients. For example, say you have three MQTT5 clients all subscribed to the same Shared Subscription group and topic. If five messages are sent to the Shared Subscription topic, the messages will likely be delivered in the following order:
* Message 1 -> Client one
* Message 2 -> Client two
* Message 3 -> Client three
* Message 4 -> Client one
* Message 5 -> Client two
* etc...

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/test/topic",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$share/*/test/topic"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/test/topic",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$share/*/test/topic"
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

Note that in a real application, you may want to avoid the use of wildcards in your ClientID and shared subscription group names/identifiers. Wildcards should only be used selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

To Run this sample using a direct MQTT connection with a key and certificate, use the following command:

```sh
# For Windows: replace 'python3' with 'python'
python3 mqtt5_shared_subscription.py --endpoint <endpoint> --cert <file> --key <file>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
# For Windows: replace 'python3' with 'python'
python3 mqtt5_shared_subscription.py --endpoint <endpoint> --cert <file> --key <file> --ca_file <file>
```

Finally, you can also set the Shared Subscription group identifier and topic with `--group_identifier` and `--topic` respectively:

```sh
# For Windows: replace 'python3' with 'python'
python3 mqtt5_shared_subscription.py --endpoint <endpoint> --cert <file> --key <file> --group_identifier <group identifier> --topic <topic>
```
