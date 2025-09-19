# Migrate from v1 to v2 of the AWS IoT SDK for Python

The AWS IoT SDK for Python v2 is a major rewrite of the v1 SDK code base built on top of Python 3.7+.
It includes many updates, such as improved consistency, ease of use, more detailed information about client status,
an offline operation queue control, etc. This guide describes the major features that are new in the v2 SDK,
and provides guidance on how to migrate your code to v2 from v1 of the AWS IoT SDK for Python.

>[!NOTE]
> If you can't find the information you need in this guide, visit the [Hot to get help](#how-to-get-help) section for
> more help and guidance.


* [What's new in AWS IoT Device SDK for Python v2](#whats-new-in-aws-iot-device-sdk-for-python-v2)
* [How to get started with AWS IoT Device SDK for Python v2](#how-to-get-started-with-aws-iot-device-sdk-for-python-v2)
    * [MQTT protocol](#mqtt-protocol)
    * [Client builder](#client-builder)
    * [Client start](#client-start)
    * [Connection types and features](#connection-types-and-features)
    * [Lifecycle events](#lifecycle-events)
    * [Publish](#publish)
    * [Subscribe](#subscribe)
    * [Unsubscribe](#unsubscribe)
    * [Client stop](#client-stop)
    * [Reconnects](#reconnects)
    * [Offline operations queue](#offline-operations-queue)
    * [Operation timeouts](#operation-timeouts)
    * [Logging](#logging)
    * [Client for AWS IoT Device Shadow](#client-for-aws-iot-device-shadow)
    * [Client for AWS IoT Jobs](#client-for-aws-iot-jobs)
    * [Client for AWS IoT fleet provisioning](#client-for-aws-iot-fleet-provisioning)
    * [Example](#example)
* [How to get help](#how-to-get-help)
* [Appendix](#appendix)
    * [MQTT5 features](#mqtt5-features)


## What's new in AWS IoT Device SDK for Python v2

* The v2 SDK client is truly async. Operations return `concurrent.futures.Future` objects.
    Blocking calls can be emulated by waiting for the returned `Future` object to be resolved.
* The v2 SDK provides implementation for MQTT5 protocol, the next step in evolution of the MQTT protocol.
* The v2 SDK supports AWS Iot services such as Fleet Provisioning.

## How To Get Started with AWS Iot Device SDK for python v2

Public APIs for almost all actions and operations has changed significantly.
There are differences between the v1 SDK and the v2 SDK. This section describes the changes you need to apply to your
project witht the v1 SDK to start using the v2 SDK.\
For more information about MQTT5, visit [MQTT5 User Guide](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md)

### MQTT Protocol

The v1 SDK uses an MQTT version 3.1.1 client under the hood.

The v2 SDK provides MQTT version 3.1.1 and MQTT version 5.0 client implementations.
This guide focuses on the MQTT5 because this version is a significant improvement over MQTT3.
For more information, see the [MQTT5 features](#mqtt5-features) section.

### Client Builder

To access AWS IoT services, you must initialize an MQTT client.

In the v1 SDK, the [AWSIoTPythonSDK.MQTTLib.AWSIotMqttClient](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient)
class represents an MQTT client. You instantiate the client directly passing all the required parameters
to the class constructor.
It's possible to change client settings after its creation using `configure*` methods,
like `configureMQTTOperationTimeout` or `configureConnectDisconnectTimeout`.

In the v2 SDK, the [awcrt.mqtt5.Client](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client)
class represents an MQTT client, specifically for MQTT5 protocol.
The v2 SDK provides an [awsiot.mqtt5_client_builder](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html)
designed to easily create common configuration types such as direct MQTT or WebSocket connections.
After and MQTT5 client is built and finalized, the settings of the resulting MQTT5 client cannot be modified.

#### Example of creating a client in the v1 SDK

```python
clientEndpoint = "<prefix>-ats.iot.<region>.amazonaws.com"
clientId = "<unique client id>"
certificateFile = "<certificate file>"  # X.509 based certificate file
privateKeyFile = "<private key file>"   # PEM encoded private key file
rootCAPath = "<root CA path>"

client = AWSIoTMQTTClient(clientId)
client.configureEndpoint(host, port)
client.configureCredentials(rootCAPath, privateKeyFile, certificateFile)

client.connect()

```

#### Example of creating a client in the v2 SDK

The v2 SDK supports different connection types. Given the same input parameters as in the v1 example above,
the most recommended method to create an MQTT5 client will be [awsiot.mqtt5_client_builder.mtls_from_path](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html#awsiot.mqtt5_client_builder.mtls_from_path).

```python
clientEndpoint = "<prefix>-ats.iot.<region>.amazonaws.com"
clientId = "<unique client id>"
certificateFile = "<certificate file>"  # X.509 based certificate file
privateKeyFile = "<private key file>"   # PEM encoded private key file

mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint=clientEndpoint,
        cert_filepath=certificateFile,
        pri_key_filepath=privateKeyFile,
        client_id=clientId,
        clean_session=False,
        keep_alive_secs=30)

mqtt5_client.start()

```
For more information, refer to the [Connection Types and Features](#connection-types-and-features) section for other
connection types supported by the v2 SDK

### Client start

To connect to the server in the v1 SDK, you call the `connect` method on an `MQTTClient` instance.

The v2 SDK changed API terminology. You `Start` the MQTT5 client rather than `Connect` as in the v1 SDK. This removes
the semantinc confusion between client-level controls and internal recurrent networking events related to connection.

#### Example of connecting to a server in the v1 SDK

```python
client = AWSIoTMQTTClient(clientId)
client.connect()

```

#### Example of connecting to a server in the v2 SDK

```python
mqtt5_client = mqtt5_client_builder.mtls_from_path( ... )
mqtt5_client.start()

```

### Connection Types and Features

The v1 SDK supports three types of connections to the AWS IoT service:
MQTT with X.509 certificate, [Amazon Cognito](https://aws.amazon.com/cognito/), and MQTT over Secure WebSocket with SigV4 authentication.

The v2 SDK adds a collection of connection types and cryptography formats
(e.g. [PKCS #11](https://en.wikipedia.org/wiki/PKCS_11) and
[Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html)),
credential providers (e.g. [Windows Certificate Store](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores)),
and other connection-related features.

For more information, refer to the [How to setup MQTT5 builder based on desired connection method](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#how-to-create-a-mqtt5-client-based-on-desired-connection-method)
section fo the MQTT5 user guide for detailed information and code snippets on each connection type and connection
feature.

| Connection type/feature                                | v1 SDK                                            | v2 SDK                             | User guide |
|--------------------------------------------------------|---------------------------------------------------|------------------------------------|:----------:|
|MQTT over Secure WebSocket with AWS SigV4 authentication| $${\Large\color{green}&#10004;}$$   	             | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#mqtt-over-websockets-with-sigv4-authentication)|
|Websocket Connection with Cognito Authentication Method | $${\Large\color{green}&#10004;}$$ 	               | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#mqtt-over-websockets-with-cognito-authentication)|
|MQTT with X.509 certificate based mutual authentication | $${\Large\color{green}&#10004;}$$     	           | $${\Large\color{green}&#10004;}$$  |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#direct-mqtt-with-x509-based-mutual-tls)|
|MQTT with Custom Authorizer Method	                     | $${\Large\color{orange}&#10004;}$$<sup>\*</sup>   | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#direct-mqtt-with-custom-authentication)|
|HTTP Proxy	                                             | $${\Large\color{orange}&#10004;}$$<sup>\*\*</sup> | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#adding-an-http-proxy)|
|MQTT with PKCS12 Method                                 | $${\Large\color{red}&#10008;}$$      	            | $${\Large\color{green}&#10004;}$$  |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#direct-mqtt-with-pkcs12-method)  |
|MQTT with Windows Certificate Store Method	             | $${\Large\color{red}&#10008;}$$  	                | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#direct-mqtt-with-windows-certificate-store-method)|
|MQTT with PKCS11 Method	                             | $${\Large\color{red}&#10008;}$$  	                | $${\Large\color{green}&#10004;}$$	 |[link](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#direct-mqtt-with-pkcs11-method)|

${\Large\color{orange}&#10004;}$<sup>\*</sup> - To get this connection type work in the v1 SDK, you need to implement
  the [Custom Authentication workflow](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authorizer.html).\
${\Large\color{orange}&#10004;}$<sup>\*\*</sup> - The v1 SDK does not allow to specify HTTP proxy,
  it is possible to configure systemwide proxy.

### Lifecycle Events

Both the v1 and the v2 SDKs provide lifecycle events for the MQTT clients.

The v1 SDK provides 2 lifecycle events: “on Online” and “on Offline”. You can supply a custom callback function via
callbacks to `AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient`.
It is recommended to use lifecycle events callbacks to help determine the state of the MQTT client during operation.

The v2 SDK adds 3 new lifecycle events, providing 5 lifecycle events in total: “on connection success”,
“on connection failure”, “on disconnect”, “on stopped”, and “on attempting connect”.

For more information, refer to the [MQTT5 user guide](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#how-to-create-a-mqtt5-client-based-on-desired-connection-method).

#### Example of setting lifecycle events in the v1 SDK

```python
def myConnectCallback(mid, data):
    return

def myDisconnectCallback(mid, data):
    return

client = AWSIoTMQTTClient(clientId)
client.onOnline = on_online_callback
client.onOffline = on_offline_callback

client.configureConnectDisconnectTimeout(10)  # 10 sec
client.connect()

```

#### Example of setting lifecycle events in the v2 SDK

```python
def on_lifecycle_connection_success(
        lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    return

def on_lifecycle_connection_failure(
        lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    return

def on_lifecycle_stopped(
        lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    return

def on_lifecycle_disconnection(
        lifecycle_disconnect_data: mqtt5.LifecycleDisconnectData):
    return

on_lifecycle_attempting_connect(
        lifecycle_attempting_connect_data: mqtt5.LifecycleAttemptingConnectData):
    return

mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
        on_lifecycle_disconnection=on_lifecycle_disconnection,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure)
mqtt5_client.start()

```

### Publish

The v1 SDK provides two API calls for publishing: blocking and non-blocking.
For the non-blocking version, the result of the publish operation is reported via a set of callbacks.
If you try to publish to a topic that is not allowed by a policy, AWS IoT Core service will close the connection.

The v2 SDK provides only asynchronous non-blocking API.
[awscrt.mqtt5.PublishPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket)
object that contains a description of the PUBLISH packet.
The [publish](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.publish)
operation takes a `PublishPacket` instance and returns a promise that contains a
[awscrt.mqtt5.PublishCompletionData](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishCompletionData).
The returned `PublishCompletionData` will contain different data depending on the `QoS` used in the publish.

> [!NOTE]
> If you try to publish with the v2 MQTT5 client to a topic that is not allowed by a policy, you do not get the
> connection
> closed but instead receive a PUBACK with a reason code.

* For QoS 0 (AT\_MOST\_ONCE): Calling `result` will return with no data
    and the promise will be complete as soon as the packet has been written to the socket.
* For QoS 1 (AT\_LEAST\_ONCE): Calling `result` will return a
    [awscrt.mqtt5.PubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PubackPacket)
    and the promise will be complete as soon as the PUBACK is received from the broker.

If the operation fails for any reason before these respective completion events,
the promise is rejected with a descriptive error. You should always check the reason code of a
[awscrt.mqtt5.PubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PubackPacket)
completion to determine if a QoS 1 publish operation actually succeeded.

#### Example of publishing in the v1 SDK

```python
# Blocking.
client.publish("my/topic", "hello", 0)
```

```python
# Non-blocking API.
client.configureMQTTOperationTimeout(30) # 30 Seconds
client.connect()

def ack_callback(mid, data=data):
    return

client.publishAsync(
        "my/topic",
        "hello",
        1,
        ackCallback=myPubackCallback)

```

#### Example of publishing in the v2 SDK

```python
publish_future,packet_id = client.publish(
        mqtt5.PublishPacket(
                topic="my/topic",
                payload=json.dumps("hello"),
                qos=mqtt5.QoS.AT_LEAST_ONCE))
publish_future.result(20) # 20 seconds

```

### Subscribe

The v1 SDK provides blocking and non-blocking API for subscribing.
To subscribe to a topic in the v1 SDK, you should provide a `topic` string to the
[subscribe](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.subscribe)
and [subscribeAsync](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html?highlight=subscribe#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.subscribeAsync)
operations. A callback parameter function will be called on receiving a new message.
If you try to subscribe to a topic that is not allowed by a policy, AWS IoT Core service will close the connection.

The v2 SDK provides only asynchronous non-blocking API. First, you need to create a
[SubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubscribePacket) object.
If you specify multiple topics in the [*Sequence*\[*Subscription*\]](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Subscription)
parameter, the v2 SDK will subscribe to all of these topics using one request.
The [subscribe](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.subscribe) operation takes a
description of the `SubscribePacket`
you wish to send and returns a promise that resolves successfully with the
corresponding [SubackPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubackPacket)
returned by the broker. The promise is rejected with an error if anything goes wrong before
the `SubackPacket` is received.
You should always check the reason codes of a `SubackPacket` completion to determine if
the subscribe operation actually succeeded.

> [!NOTE]
> If you try to subscribe with the v2 MQTT5 client to a topic that is not allowed by a policy, you do not get the
> connection
> closed but instead receive a SUBACK with a reason code.

In the v2 SDK, if the MQTT5 client is going to subscribe and receive packets from the MQTT broker,
it is important to also setup the `on_publish_received` callback int the `ClientOptions`.
This callback is invoked whenever the client receives a message from the server on a topic the client is subscribed to.
With this callback, you can process messages made to subscribed topics through its `message` parameter
[PublishReceivedData](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishReceivedData).

#### Example of subscribing in the v1 SDK

```python
client.configureMQTTOperationTimeout(30) # 30 Seconds

def ackCallback(mid, data):
    return

def messageCallback(client, userdata, message):
    return

# blocking
client.subscribe(
        "myTopic/#",
        1,
        callback=messageCallback)

# Non blocking
client.subscribeAsync(
        "myTopic/#",
        1,
        ackCallback=ackCallback,
        messageCallback=messageCallback)

```

#### Example of subscribing in the v2 SDK

```python

def on_publish_received(publish_received_data):
    return

client_options = mqtt5.ClientOptions( ... )
client_options.on_publish_received = on_publish_received
client = mqtt5.Client(client_options)

subscribe_future = client.subscribe(
        subscribe_packet=mqtt5.SubscribePacket(
                subscriptions=[mqtt5.Subscription(
                topic_filter="my/own/topic",
                qos=mqtt5.QoS.AT_LEAST_ONCE)]))

suback = subscribe_future.result(20)

```

### Unsubscribe

The v1 SDK provides blocking and non-blocking APIs for unsubscribing. To unsubscribe from a topic in the v1 SDK,
you should provide a topic string to the
[unsubscribe](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html?highlight=unsubscribe#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.unsubscribe)
or [unsubscribeAsync](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html?highlight=unsubscribe#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.unsubscribeAsync)
operations. The asynchronous operation call the passed callback which determines success of failure.

The v2 SDK provides only asynchronous non-blocking API.
First, you need to create an [UnsubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubscribePacket)
object. The [unsubscribe](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.unsubscribe)
operation takes a description of the [UnsubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubscribePacket)
you wish to send and returns a promise that resolves successfully with the corresponding
[UnsubackPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket)
returned by the broker. The promise is rejected with an error if anything goes wrong before
the [UnsubackPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket) is received.
You should always check the reason codes of
a [UnsubackPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket) completion
to determine if the unsubscribe operation actually succeeded.

Similar to subscribing, you can unsubscribe from multiple topics in one request by passing
a list of topics to topic\_filters (\*Sequence[str\*\*]) in \*[\*UnsubackPacket\*](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket)

#### Example of unsubscribing in the v1 SDK

```python
# Blocking API.
client.unsubscribe("my/topic")
client.unsubscribe("another/topic")

```

```python
# Non-blocking API.
def unsuback_callback(mid):
    return

client.unsubscribeAsync("my/topic", ackCallback=unsuback_callback)

```

#### Example of unsubscribing in the v2 SDK

```python
unsubscribe_future = mqtt5_client.unsubscribe(
        unsubscribe_packet=mqtt5.UnsubscribePacket(
                topic_filters=["my/topic"]))
unsuback = unsubscribe_future.result(60) # 60 Seconds
print("Unsubscribed with {}".format(unsuback.reason_codes))

```

### Client stop

In the v1 SDK, the `disconnect` method in the `AWSIotMqttClient` class disconnects the client. Once disconnected,
the client can connect again by calling `connect`.

In the v2 SDK, an MQTT5 client can stop a session by calling the
[stop](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.stop) method.
You can provide an optional [DisconnectPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectPacket)
parameter. A closed client can be started again by calling
[start](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.start).


#### Example of disconnecting a client in the v1 SDK

```python
client.disconnect();

```

#### Example of disconnecting a client in the v2 SDK

```python
mqtt5_client.stop(
        disconnect_packet=mqtt5.DisconnectPacket(
                reason_code=mqtt5.DisconnectReasonCode.NORMAL_DISCONNECTION,
                session_expiry_interval_sec=3600))

```

### Reconnects

The v1 SDK attempts to reconnect automatically using a [Progressive Reconnect Back Off](https://github.com/aws/aws-iot-device-sdk-python/blob/master/README.rst#progressive-reconnect-back-off)
until connection succeeds or `client.disconnect()` is called.

The v2 SDK attempts to reconnect automatically until the connection succeeds or `client.stop()` is called.
The reconnection parameters, such as min/max delays and
[jitter modes](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ExponentialBackoffJitterMode),
are configurable through [awsiot.mqtt5\_client\_builder](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html#module-awsiot.mqtt5_client_builder).


#### Example of tweaking reconnection settings in v1

```python
baseReconnectQuietTimeSecond = 1 # Initial backoff time
maxReconnectQuiteTimeSecond = 23 # maximum backoff time
stableConnectionTimeSecond = 20  # the time the connection is considered stable
client.configureAutoReconnectBackoffTime(
        baseReconnectQuietTimeSecond,
        maxReconnectQuiteTimeSecond,
        stableConnectionTimeSecond)

```

#### Example of tweaking reconnection settings in the v2 SDK

```python
mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
 ...
        max_reconnect_delay_ms=200,
        min_reconnect_delay_ms=200,
        min_connected_time_to_reset_reconnect_delay_ms=200,
        retry_jitter_mode=mqtt5.ExponentialBackoffJitterMode.FULL)

mqtt5_client.start()

```

### Offline Operations Queue

In the v1 SDK, if you're having too many in-flight QoS 1 messages, all extra messages will be queued for them to
be sent at a later time, when the number of in-flight messages goes below the so-called in-flight publish limit.
By default, the v1 SDK supports a maximum of 20 in-flight operations.

The v2 SDK does not limit the number of in-flight messages.
Additionally, the v2 SDK provides a way to configure which kind of packets will be placed into the offline queue
when the client is in the disconnected state. The following code snippet demonstrates how to enable storing all packets
except QOS0 publish packets in the offline queue on disconnect:

#### Example of configuring the offline queue in the v2 SDK

```python
mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
 ...
        offline_queue_behavior=
            mqtt5.ClientOperationQueueBehaviorType.FAIL_QOS0_PUBLISH_ON_DISCONNECT)

mqtt5_client.start()

```

> [!NOTE]
> AWS IoT Core [limits the number of allowed operations per second](https://docs.aws.amazon.com/general/latest/gr/iot-core.html#message-broker-limits).
> The [get_stats](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.get_stats) method returns
> the current state of an `awscrt.mqtt5.Client` object's queue of operations in
> [OperationStatisticsData](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.OperationStatisticsData),
> which may help with tracking the number of in-flight messages.

``` python
op_stats_data = mqtt5_client.get_stats()
print(
    "Client operations queue statistics:\n" +
    "incomplete_operation_count:" + op_stats_data.incomplete_operation_count() + "\n"
    "incomplete_operation_size: " + op_stats_data.incomplete_operation_size() + "\n"
    "unacked_operation_count: " + op_stats_data.unacked_operation_count() + "\n"
    "unacked_operation_size: " + op_stats_data.unacked_operation_size() + "\n")

```

For more information, see [withOfflineQueueBehavior documentation](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions).

For the list of the supported offline queue behaviors and their descriptions,
see [ClientOfflineQueueBehavior types documentation](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOperationQueueBehaviorType).

### Operation Timeouts

In the v1 SDK, all operations (*publish*, *subscribe*, *unsubscribe*) will take a timeout for all of them.

In the v2 SDK, operations timeout is set for the MQTT5 client with the
[ClientOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions)
class member `ack_timeout_sec`.
The default value is no timeout. Failing to set a timeout can cause an operation to stuck forever,
but it won't block the client.

The [get\_stats](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.get_stats) method returns
the current state of an` mqtt5.Client` object's queue of operations, which may help with tracking operations.

#### Example of timeouts in the v1 SDK

```python
connectTimeoutSec = 10
client.configureConnectDisconnectTimeout(connectTimeoutSec)
client.connect();

publishTimeoutMs = 20
client.configureMQTTOperationTimeout(publishTimeoutMs)
client.publish("my/topic", "hello", 1)

```

### Example of timeouts in the v2 SDK

```python
mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
        ack_timeout_sec=20)

```

### Logging

The v1 SDK uses `AWSIoTPythonSDK.core` custom logger for logging.

The v2 SDK uses  the logging facility provided by the [crt-io](https://awslabs.github.io/aws-crt-python/api/io.html)

#### Example of using logging in the v1 SDK

```python
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.error("error log")
logger.info("info log")

```

#### Example of using logging in the v2 SDK

```python
from awscrt import io

io.init_logging(log_level=io.LogLevel.Trace, file_name='stderr')

logger.debug("error log")

```

### Client for AWS IoT Device Shadow

The v1 SDK is built with [AWS IoT device shadow support](http://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-shadows.html),
which provides access to thing shadows (sometimes referred to as device shadows).

The v2 SDK also supports device shadow service, but with a completely different APIs.
First, you subscribe to special topics to get data and feedback from a service.
The service client provides API for that. For example, `subscribe_to_get_shadow_accepted` subscribes to a topic
to which AWS IoT Core will publish a shadow document. The server will notify you if it cannot send you a
requested documen via the `subscribe_to_get_shadow_rejected`.\
After subscribing to all the required topics, the service client can start interacting with the server,
for example update the status or request for data. These actions are also performed via client API calls.
For example, `publish_get_shadow` sends a request to AWS IoT Core to get a shadow document.
The requested Shadow document will be received in a callback specified in the `subscribe_to_get_shadow_accepted` call.

AWS IoT Core [documentation for Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html)
service provides detailed descriptions for the topics used to interact with the service.

#### Example of creating a Device Shadow service client in the v1 SDK

```python
# Blocking and non-blocking API.
shadow_client= AWSIoTMQTTShadowClient("<client id">)
shadow_client.configureEndpoint("<hostname>", port)
shadow_client.configureCredentials(
        rootCAPath,
        privateKeyPath,
        certificatePath)
shadow_client.connect()
isPersistentSubscribe ** = True
deviceShadowHandler = shadow_client.createShadowHandlerWithName(
        "<shadow name>",
        *isPersistentSubscribe*)

```

#### Example of creating a Device Shadow service client in the v2 SDK

```python
mqtt5_client.start()
shadow_client = iotshadow.IotShadowClient(mqtt5_client)

```

#### Example of deleting a Device Shadow in the v1 SDK

```python
# Delete Shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    return
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

```

#### Example of deleting a Classic Shadow in the v2 SDK

```python
def delete_accepted(DeleteShadowResponse response):
    return
shadow_client.subscribe_to_delete_shadow_accepted(request, qos, callback)

def delete_rejected(DeleteShadowResponse response):
    return
shadow_client.subscribe_to_delete_shadow_rejected(request, qos, callback)

iotshadow.DeleteShadowRequest req
req.client_token = "<client token>"
req.thing_name = "<thing name>"

shadow_future = shadow_client.publish_delete_shadow(
        request=req,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

```

#### Example of updating a Classic Shadow in the v1 SDK

```python
# Update Shadow
def customShadowCallback_Update(payload, responseStatus, token):
    return

JSONPayload = '{"state":{"desired":{"property":' + str(3) + '}}}'
deviceShadowHandler.shadowUpdate(
        JSONPayload,
        customShadowCallback_Update,
        5)

```

#### Example of updating a Classic Shadow in the v2 SDK

```python
# Update shadow
def on_update_shadow_accepted(response):
    return
 update_accepted_subscribed_future, _ =
        shadow_client.subscribe_to_update_shadow_accepted(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                        thing_name=shadow_thing_name),
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_update_shadow_accepted)

def on_update_shadow_rejected(error):
    return
update_rejected_subscribed_future, _ =
        shadow_client.subscribe_to_update_shadow_rejected(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                        thing_name=shadow_thing_name),
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_update_shadow_rejected)

request = iotshadow.UpdateShadowRequest(
        thing_name="thing name",
        state=iotshadow.ShadowState(
                reported={color: 1},
                desired={color: 2},),
        client_token="<token>")

future = shadow_client.publish_update_shadow(
        request,
        mqtt5.QoS.AT_LEAST_ONCE)

```

#### Example of subscribing to a delta Shadow events in the v1 SDK

```python
# Delta Events
shadow_client.connect()

def customShadowCallback_Delta(payload, responseStatus, token):
    return

deviceShadowHandler = shadow_client.createShadowHandlerWithName(
        "<thing name>",
        True)

deviceShadowHandler.shadowRegisterDeltaCallback(
        customShadowCallback_Delta)

```

#### Example of subscribing to a delta Shadow events in the v2 SDK

```python
# Delta Events
def on_shadow_delta_updated(delta):
    return

delta_subscribed_future, _ = shadow_client.subscribe_to_shadow_delta_updated_events(
        request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(
                thing_name=shadow_thing_name),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=on_shadow_delta_updated)

delta_subscribed_future.result()

```

For more information, see API documentation for the v2 SDK
[Device Shadow](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotshadow.html).

For code examples, see the v2 SDK [Device Shadow](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/service_clients/shadow.py).


### Client for AWS IoT Jobs

The v1 SDK and the v2 SDK offer support of AWS IoT Core services implementing a service client for the
[Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) service which helps with defining a set of
remote operations that can be sent to and run on one or more devices connected to AWS IoT.


The v2 SDK Jobs service APIs are completely different than the v1 SDK APIs.
The Jobs service client provides API similar to API provided by [Client for Device Shadow Service](#client-for-device-shadow-service).
First, you subscribe to special topics to get data and feedback from a service.
The service client provides API for that. After subscribing to all the required topics,
the service client can start interacting with the server, for example update the status or request for data.
These actions are also performed via client API calls.


#### Example creating a jobs client in the v1 SDK

```python
jobs_client = AWSIoTMQTTThingJobsClient(
        "<client id>",
        "<thing name>",
        QoS=1,
        awsIoTMQTTClient=mqtt_client)

jobsClient.connect()

```

#### Example creating a jobs client in the v2 SDK

```python
mqtt5_client.start()

jobs_client = iotjobs.IotJobsClient(mqtt5_client)

```

#### Example subscribing to jobs topics in the v1 SDK

```python
# Blocking API
def newJobReceived(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        newJobReceived,
        jobExecutionTopicType.
        JOB_NOTIFY_NEXT_TOPIC)

def startNextJobSuccessfullyInProgress(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        startNextJobSuccessfullyInProgress,
        jobExecutionTopicType.JOB_START_NEXT_TOPIC,
        jobExecutionTopicReplyType.JOB_ACCEPTED_REPLY_TYPE)

def startNextRejected(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        startNextRejected,
        jobExecutionTopicType.JOB_START_NEXT_TOPIC,
        jobExecutionTopicReplyType.JOB_REJECTED_REPLY_TYPE)

def updateJobSuccessful(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        updateJobSuccessful,
        jobExecutionTopicType.JOB_UPDATE_TOPIC,
        jobExecutionTopicReplyType.JOB_ACCEPTED_REPLY_TYPE,
        '+')

def updateJobRejected(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        updateJobRejected,
        jobExecutionTopicType.JOB_UPDATE_TOPIC,
        jobExecutionTopicReplyType.JOB_REJECTED_REPLY_TYPE,
        '+')

def describeTopic(mqtt_client, userdata, message):
    return

jobs_client.createJobSubscription(
        describeTopic,
        jobExecutionTopicType.JOB_DESCRIBE_TOPIC,
        jobExecutionTopicReplyType.JOB_REJECTED_REPLY_TYPE,
        jobId)

```

```python
# Non blocking API

def ackCallback(mid, data):
    return

def cllback(client, userdata, message):
    return

packet_id = jobs_client.createJobSubscriptionAsync(
        ackCallback=ackCallback,
        callback=callback,
        jobExecutionType=jobExecutionTopicType.JOB_WILDCARD_TOPIC,
        jobReplyType=jobExecutionTopicReplyType.JOB_REQUEST_TYPE,
        jobId=None)

```

#### Example subscribing to jobs topics in the v2 SDK

More subscriptions will be listed with their corresponding API

```python

# Subscribe to necessary topics
changed_subscription_request = iotjobs.NextJobExecutionChangedSubscriptionRequest(
        thing_name="<thing name>")

def on_next_job_execution_changed(event):
    return

subscribed_future, _ = jobs_client.subscribe_to_next_job_execution_changed_events(
        request=changed_subscription_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=on_next_job_execution_changed)

changed_subscription_request = iotjobs.JobExecutionChangedSubscriptionRequest(
        thing_name="<thing name>")

def on_job_execution_changed(event):
    return

subscribed_future, _  = jobs_client.subscribe_to_job_executions_changed_events(
        request=changed_subscription_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=on_job_execution_changed)

```

#### Example of execution of the next pending job in the v1 SDK

```python
# start next job
statusDetails =
        {'StartedBy': 'ClientToken: {} on {}'.format(
                clientToken,
                datetime.datetime.now().isoformat())}

jobs_client.sendJobsStartNext(
                 statusDetails=statusDetails)
```

#### Example of execution of the next pending job in the v2 SDK

```python
start_subscription_request = iotjobs.StartNextPendingJobExecutionSubscriptionRequest(thing_name="thing name")

def on_start_next_pending_job_execution_accepted(response):
    return

subscribed_accepted_future, _ =
        jobs_client.subscribe_to_start_next_pending_job_execution_accepted(
                request=start_subscription_request,
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_start_next_pending_job_execution_accepted)

def on_start_next_pending_job_execution_rejected(rejected):
    return

subscribed_rejected_future, _ =
        jobs_client.subscribe_to_start_next_pending_job_execution_rejected(
                request=start_subscription_request,
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_start_next_pending_job_execution_rejected)

execution_request = iotjobs.StartNextPendingJobExecutionRequest(
        thing_name="thing_name")

publish_future = jobs_client.publish_start_next_pending_job_execution(
        request=execution_request,
        mqtt.QoS.AT_LEAST_ONCE)

publish_future.add_done_callback(on_publish_start_next_pending_job_execution)

```

#### Example of getting detailed information about a job in the v1 SDK

```python
# get info for specific job id
jobs_client.sendJobsDescribe(jobId = "job id", executionNumber=1, includeJobDocument=True)

# or for the next job id
jobs_client.sendJobsDescribe(jobId = '$next', executionNumber=1, includeJobDocument=True)

```

#### Example of getting detailed information about a job in the v2 SDK

```python
def accepted_callback(response) # DescribeJobExecutionResponse
    # job details received
    return

def rejected_callback(RejectedError response) # RejectedError
    # error getting job details
    return

iotjobs.DescribeJobExecutionSubscriptionRequest request;
request.job_id = "job id"
request.thing_name = "thing name"

jobs_client.subscribe_to_describe_job_execution_accepted(
        request=request,
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=acceted_callback)

jobs_client.subscribe_to_describe_job_execution_rejected(
        request=request,
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=rejected_callback)

describe_request = iotjobs.DescribeJobExecutionRequest(
        client_token="client token",
        execution_number=23,
        include_job_document=false,
        job_id="job id",
        thing_name="thing name")

jobs_client.publish_describe_job_execution(
        request=describe_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

```

#### Example updating status of a job on the v1 SDK

```python
statusDetails = {'HandledBy': 'aws iot sdk'}

jobs_client.sendJobsUpdate(
        jobId="<job id>",
        status=jobExecutionStatus.JOB_EXECUTION_SUCCEEDED,
        statusDetails=statusDetails,
        expectedersion=4,
        executionNumber=3,
        includeJobExecutionState=False,
        includeJobDocument=False
        stepTimeoutInMinutes=3)

```

#### Example updating status of a job in the v2 SDK

```python
update_subscription_request = iotjobs.UpdateJobExecutionSubscriptionRequest(
        thing_name=jobs_thing_name,
        job_id='+')

def on_update_job_execution_accepted(response):
    return

subscribed_accepted_future, _ =
        jobs_client.subscribe_to_update_job_execution_accepted(
                request=update_subscription_request,
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_update_job_execution_accepted)

def on_update_job_execution_rejected(rejected):
    return

subscribed_rejected_future, _ =
        jobs_client.subscribe_to_update_job_execution_rejected(
                request=update_subscription_request
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_update_job_execution_rejected)

update_job_execution_request = iotjobs.UpdateJobExecutionRequest(
        client_token="client_token",
        excution_number=32,
        expected_version=23,
        include_job_document=true,
        include_job_execution_state=true,
        job_id="job id",
        status=IN_PROGRESS,
        status_details={"key":"val"},
        step_timeout_in_minutes=23,
        thing_name="thing name")

jobs_client.publish_update_job_execution(
        request=update_job_execution_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

```

#### Example of getting job info in the v1 SDK

```python
# describe next job
jobs_client.sendJobsQuery(jobExecutionTopicType.JOB_DESCRIBE_TOPIC, '$next')

# get list of pendig jobs
jobs_client.sendJobsQuery(jobExecutionTopicType.JOB_GET_PENDING_TOPIC)

```

#### Example of getting job info in the v2 SDK

```python
def on_get_pending_job_executions_accepted(response):
    return

jobs_request_future_accepted, _ =
        jobs_client.subscribe_to_get_pending_job_executions_accepted
                request=get_jobs_request,
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_get_pending_job_executions_accepted)

def on_get_pending_job_executions_rejected(error):
    return

jobs_request_future_rejected, _ =
        jobs_client.subscribe_to_get_pending_job_executions_rejected(
                request=get_jobs_request,
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                callback=on_get_pending_job_executions_rejected)

get_jobs_request = iotjobs.GetPendingJobExecutionsRequest(thing_name="<thing name">)

get_jobs_request_future = jobs_client.publish_get_pending_job_executions(
        request=get_jobs_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

```

For detailed descriptions for the topics used to interact with the service, see AWS IoT Core documentation for the
[Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/jobs-mqtt-api.html) service.

For more information about the service clients, see API documentation for the v2 SDK
[Jobs](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotjobs.html).

For code examles, see [Jobs](https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/service_clients/jobs.py)
samples.


### Client for AWS IoT fleet provisioning

[Fleet Provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)
(also known as Identity Service) is another AWS IoT service that the v2 SDK provides access to.
By using AWS IoT fleet provisioning, AWS IoT can generate and securely deliver device certificates and private keys
to your devices when they connect to AWS IoT for the first time.

The Fleet Provisioning service client provides APIs similar to the APIs provided by
[Client for Device Shadow Service](#client-for-device-shadow-service).
First, you subscribe to special topics to get data and feedback from a service.
The service client provides APIs for that. After subscribing to all the required topics,
the service client can start interacting with the server, for example update the status or request for data.
These actions are also performed via client API calls.

For detailed descriptions for the topics used to interact with the Fleet Provisioning service, see
AWS IoT Core documentation for [Fleet Provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html)

For more information about the Fleet Provisioning service client, See API documentation for the v2 SDK
[Fleet Provisioning](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotidentity.html).

For code examples, see the v2 SDK [Fleet Provisioning](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/service_clients/fleet_provisioning_basic.md)
samples.


### Example

It's always helpful to look at a working example to see how new functionality works, to be able to tweak different options,
to compare with existing code. For that reason, we implemented a
[X509 Publish/Subscribe example](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt/mqtt5_x509.md)
([source code](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt/mqtt5_x509.py))
in the v2 SDK similar to a sample provided by the v1 SDK (see a corresponding
[readme section](https://github.com/aws/aws-iot-device-sdk-python/blob/master/README.rst#basicpubsub) and
[source code](https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py)).

## How to get help

Questions? you can look for an answer in the
[discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions) page.
Or, you can always open a [new discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions/new?category=q-a&labels=migration),
and we will be happy to help you.

## Appendix

### MQTT5 Features

**Clean Start and Session Expiry**\
You can use Clean Start and Session Expiry to handle your persistent sessions with more flexibility.
For more information, see the [awscrt.mqtt5.ClientSessionBehaviorType](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientSessionBehaviorType)
enum and the [NegotiatedSettings.session_expiry_interval_sec](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.NegotiatedSettings)
method.

**Reason Code on all ACKs**\
You can debug or process error messages more easily using the reason codes.
Reason codes are returned by the message broker based on the type of interaction with the broker
(Subscribe, Publish, Acknowledge).
For more information, see [PubAckReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PubackReasonCode),
[SubackReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubackReasonCode),
[UnsubackReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubackReasonCode),
[ConnectReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnectReasonCode),
[DisconnectReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectReasonCode).

**Topic Aliases**\
You can substitute a topic name with a topic alias, which is a two-byte integer.
Use [mqtt5.TopicAliasingOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.TopicAliasingOptions)
with [mqtt5.ClientOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions),
when creating a [PUBLISH](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) packet,
use the parameter `topic\_alias(int)`.

**Message Expiry**\
You can add message expiry values to published messages. Use `message_expiry_interval_sec`
variable when creating a [PUBLISH packet](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket).

**Server disconnect**\
When a disconnection happens, the server can proactively send the client a `DISCONNECT` to notify connection closure
with a reason code for disconnection.\
For more information, see the [DisconnectPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectPacket)
class.

**Request/Response**\
Publishers can request a response be sent by the receiver to a publisher-specified topic upon reception.
Use `response_topic` method in
[PublishPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) class.

**Maximum Packet Size**\
Client and Server can independently specify the maximum packet size that they support.\
For more information, see [ConnectPacket.maximum_packet_size(int)](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnectPacket),
the [NegotiatedSettings.maximum_packet_size_to_server](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.NegotiatedSettings),
and the [ConnAckPacket.maximum_packet_size](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnackPacket) methods.

**Payload format and content type**\
You can specify the payload format (binary, text) and content type when a message is published.
These are forwarded to the receiver of the message. Use content\_type(str) method in
[PublishPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) class.

**Shared Subscriptions**\
Shared Subscriptions allow multiple clients to share a subscription to a topic and only one client will receive messages
published to that topic using a random distribution.

> [!NOTE]
> AWS IoT Core supports Shared Subscriptions for both MQTT3 and MQTT5. For more information,
> see [Shared Subscriptions](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt5-shared-subscription)
> from the AWS IoT Core developer guide.

