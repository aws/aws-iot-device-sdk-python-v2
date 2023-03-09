# Operations Queue

[**Return to main sample list**](../README.md)

This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages through an MQTT connection. It then subscribes and begins publishing messages to a topic, like in the [PubSub sample](../PubSub/README.md).

However, this sample uses a operation queue to handle the processing of operations, rather than directly using the MQTT311 connection. This gives an extreme level of control over how operations are processed, the order they are processed in, limiting how many operations can exist waiting to be sent, what happens when a new operation is added when the queue is full, and ensuring the MQTT311 connection is never overwhelmed with too many messages at once.

Additionally, using a queue allows you to put limits on how much data you are trying to send through the socket to the AWS IoT Core server. This can help keep your application within the IoT Core sending limits, ensuring all your MQTT311 operations are being processed correctly and the socket is not backed up. It also the peace of mind that your application cannot become "runaway" and start sending an extreme amount of messages at all once, clogging the socket depending on how large the messages are and the frequency.

**Note**: MQTT5 does not have the same issues with backed up sockets due to the use of an internal operation queue, which ensures the socket does not get backed up.

This operation queue can be configured in a number of different ways to best match the needs of your application. Further, the operation queue is designed to be as standalone as possible so it can be used as a starting point for implementing your own operation queue for the MQTT311 connection. The `MqttOperationQueue` class is fully documented with comments explaining the functions used.

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/test/topic/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/test/topic/*"
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

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

To Run this sample, use the following command:

```sh
python3 samples/operation_queue/operation_queue.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
python3 samples/operation_queue/operation_queue.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key> --ca_file <path to CA file>
```

Finally, you can control how the operation queue inserts new operations and drops operations when the queue is full via the `--queue_mode` parameter. For example, to have a rolling queue where new operations are added to the front and overflow is removed from the back of the queue:

```sh
python3 samples/operation_queue/operation_queue.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key> --queue_mode 1
```

See the output of the `--help` argument for more information on the queue operation modes and configuration of this sample.


## Queue Design

The operation queue is designed to hold a number of operations (publish, subscribe, and unsubscribe) in a queue so that it can be processed in a controlled manner that doesn't overwhelm the MQTT311 connection, as well as giving a control to your code on how the operations are processed. This is written on top of the MQTT311 connection and as a sample so it can be used as a reference and extended/adjusted to meet the needs of your application.

The backbone of how the operation queue works is the [MQTT311 operation statistics](https://awslabs.github.io/aws-crt-python/api/mqtt.html#awscrt.mqtt.Connection.get_stats). [These statistics](https://awslabs.github.io/aws-crt-python/api/mqtt.html#awscrt.mqtt.OperationStatisticsData) reported by the MQTT311 connection give a window into what the MQTT311 connection is doing, what operations are being sent to AWS IoT Core via via a socket, and what operations are waiting for responses from AWS IoT Core. This is how the operation queue knows how many operations are being processed and when to send another, as well as allowing it to be reactive to the state of the connection.

Specifically, the operation statistics is how the operation queue class calculates whether or not to send another operation in its queue to the MQTT311 connection or not. If the MQTT311 connection has many operations waiting, it can hold off and wait until the MQTT311 connection has processed the data and can consume more. This has the benefits mentioned in the top of this document: It prevents the MQTT311 connection from being flooded with too many operations and the socket being too backed up. Additionally, it has the benefit of allowing your code to control the order of operations that are sent directly and can be configured so that your code has the assurance it will not send too much data and exceed AWS IoT Core limits.

Put simply, the operation queue is a system that looks at the MQTT311 operation statistics at a timed interval and determines whether the MQTT311 connection can take another operation based on the settings of the operation queue. If it can, it sends that operation to the MQTT311 client and continues to observe it's statistics until either the queue is empty and there is nothing to do, or until the operation queue is stopped.

___________

The operation queue is designed to be a helpful reference you can use directly in your applications to have a queue-based control over the MQTT operation flow, as well as ensuring that you have back pressure support and will not write too much data to the socket at a given time. The operation queue in this sample is designed to be flexible and powerful, but of course you can extend the operation queue to meet the needs of your application. For example, it could be extended to allow injecting operations at specific indexes in the queue, allow removing operations at any index in the queue, etc. All of the code for the operation queue has comments that explain what each function does for easier customization and extension.

Below is more information on specifics about how the operation queue works.

### Operations outside of the queue

What is great with using the operation statistics to determine the state of the MQTT311 connection is that if your code uses the MQTT311 connection directly for something or you are doing non-queued operations, like connect/disconnect for example, then the queue will still properly react and possibly limit the action of the queue based on what the statistics return and how your queue is setup. You can even have two operation queues on the same connection!

This is helpful because it allows you to selectively choose which operations are written to the MQTT311 connection socket right away and which are behind the queue on a per-operation basis. This means that if you have a operation that you must get sent as soon as possible regardless of any queues, you can just directly call the operation (publish, subscribe, unsubscribe, etc.) directly on the MQTT311 connection and the queue will react accordingly.

### Retried operations

A question you might be wondering is how does the operation queue, and by extension the operation statistics, handle retried QoS1 operations? QoS1 requires getting an acknowledgement (ACK) back from the MQTT server and, should this not happen, it will retry the operation by sending it again. This is why QoS1 is described as "at least once", because it only tries to guarantee that the message will be sent at **least once** but there are no guarantees that it will not be sent **more than once**.

**Note**: For operations that need to be sent exactly and only one time, QoS2 would be used for this purpose. However, at this time QoS2 is not currently supported by the AWS IoT SDKs.

For the MQTT311 connection operations (publish, subscribe, and unsubscribe), QoS1 operations will NOT be retried automatically even if the MQTT server does not send an acknowledgement. These operations will keep waiting for a reply from the server until it receives one. This can be adjusted by setting an operation timeout, in which case the operation will be resolved as having failed to send if an acknowledgment is not received in the given timeout time. Note that, by default, the MQTT311 connection will not have an operation timeout set and this timeout has to be manually set.

Connections are an exception to this however. Connections are retried automatically with an exceptional back-off if the connect does not get an acknowledgment from the server in the expected time. However, because this process is done internally by the MQTT311 connection, it would fall into the [operations outside of the queue](#operations-outside-of-the-queue) for the purposes of the operation queue.

However, there is a case where QoS1 operations (publish, subscribe, unsubscribe) will be retried, and this is when the MQTT311 connection has in-flight operations that have not received an acknowledgment from the server and the MQTT311 connection becomes disconnected from the server. When the MQTT311 connection reconnects, it will resend the QoS1 operations that were waiting for acknowledgements prior to becoming disconnected.

When a QoS1 operation is made and sent to the socket so it can go to the MQTT server, it gets added to the "in-flight" operation statistics and is removed from the "incomplete operations". If the server does not send an acknowledgement of the operation, the MQTT311 client becomes disconnected, the MQTT311 reconnects, and the operation is resent, the operation is NOT moved from the "in-flight" statistics nor is a new one added. Instead, the resent operation simply keeps waiting in the "in-flight". Finally, when the operation gets a response from the server, whether it be on the initial operation or a retry, it will be removed from the "in-flight" statistics. Likewise, if the operation has a timeout set and does not get an acknowledgement within the given timeout period, it will be removed from the "in-flight" statistics when the operation is considered to have failed.

**Note**: This only applies to QoS1 operations! QoS0 operations are different and [explained below](#qos-0-operations).

This means that for the operation queue, it has no idea if the operation has been retried or not, it just sees it as there being an in-flight operation. This means that if you have a bunch of in-flight operations all waiting, the queue will wait for the MQTT server to send acknowledgements without needing additional configurations nor code on the user side.

### QoS 0 operations

Operations can be made with either QoS0 or QoS1. QoS0 states than an operation will be sent "at most once". This means that once the operation is written to the socket, it is removed and the code does not wait to see if the server actually got the data. For the MQTT311 operation statistics, it means that a QoS0 operation is written to the socket and then immediately removed from the "incomplete operations", it does not get added to "in-flight" nor is there any waiting to be done, it is fire and forget.

For the operation queue, this means that QoS0 operations are stored in the queue and will wait like all other operations until the MQTT311 operation statistics are in a state where it can be published, but once it is published, it will be fired and forgotten. QoS0 operations will not hang around and will be fired as soon as they are in the front of the queue and the MQTT311 operation statistics are in an acceptable state.

### Service Clients (Shadow, Jobs, etc)

The operation queue should work fully alongside service clients like [Shadow](../Shadow/README.md), [Jobs](../Jobs/README.md), and [Fleet Provisioning](../Identity/README.md). These service clients ultimately subscribe, publish, and unsubscribe to MQTT topics, and as such they are compatible with the operation queue. That said though, they will **not** be added to the operation queue, instead they will function like if operations were made manually outside of the queue, as noted in the [Operations outside of the queue section](#operations-outside-of-the-queue).
