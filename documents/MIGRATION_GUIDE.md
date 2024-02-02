grate from V1 to V2 of the AWS IoT SDK for Python

The V2 AWS IoT SDK for Python is a major rewrite of the V1 code base built on top of Python 3.7+. It includes many updates, such as improved consistency, ease of use, more detailed information about client status, an offline operation queue control, etc. This guide describes the major features that are new in V2, and provides guidance on how to migrate your code to V2 from V1.

## What’s new

* V2 SDK client is truly async. Operations return `concurrent.futures.Future` objects.
    Blocking calls can be emulated by waiting for the returned `Future` object to be resolved.
* V2 SDK provides implementation for MQTT5 protocol, the next step in evolution of the MQTT protocol.
* Public API terminology has changed. You `start()` or `stop()` the MQTT5 client rather than c`onnect` or d`isconnect` like in V1. This removes the semantic confusion with the connect/disconnect as the client-level controls vs. internal recurrent networking events.
* Support for Fleet Provisioning AWS IoT Core service.

Public API for almost all actions and operations has changed significantly. For more details about the new features and to see specific code examples, refer to the other sections of this guide.


## How To Get Started with V2 SDK

There are differences between IoT Python V1 SDK and IoT Python V2 SDK. Below are changes you need to make to use IoT Python V2 SDK features. For more information about MQTT5, visit [MQTT5 User Guide](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md)


### MQTT Protocol

V1 SDK uses an MQTT version 3.1.1 client under the hood.

V2 SDK provides MQTT version 3.1.1 and MQTT version 5.0 client implementations. This guide focuses on the MQTT5 since this version is significant improvement over MQTT3. See MQTT5 features section.


### Client Builder

To access the AWS IoT service, you must initialize an MQTT client.

In V1 SDK, the [`AWSIoTPythonSDK.MQTTLib.`AWSIotMqttClient](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient) class represents an MQTT client. You instantiate the client directly passing all the required parameters to the class constructor. It’s possible to change client settings after its creation using `configure*` methods, e.g. `configureMQTTOperationTimeout` or `configureConnectDisconnectTimeout`.

In V2 SDK, the [awcrt.mqtt5.Client](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client) class represents an MQTT client, specifically MQTT5 protocol. V2 SDK provides an [awsiot.mqtt5_client_builder](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html) designed to easily create common configuration types such as direct MQTT or WebSocket connections, the resulting MQTT5 client cannot have its settings modified.

_Example of creating a client in V1_

```
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

_Example of creating a client in V2_
V2 SDK supports different connection types. Given the same input parameters as in the V1 example above, the most suitable method to create an MQTT5 client will be [awsiot.mqtt5_client_builder.mtls_from_path](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html#awsiot.mqtt5_client_builder.mtls_from_path).

```
from awsiot import mqtt5_client_builder

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

Refer to the [Connection Types and Features](https://quip-amazon.com/RUfpAM2x5mXr#temp:C:XVAe19c32f97575498c9c9ddc15a) section for other connection types supported by V2 SDK.


### Connection Types and Features

V1 SDK supports two types of connections to connect to the AWS IoT service: MQTT with X.509 certificate and MQTT over Secure WebSocket with SigV4 authentication.

V2 SDK adds a collection of connection types and cryptography formats (e.g. [PKCS #11](https://en.wikipedia.org/wiki/PKCS_11) and [Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html)), credential providers (e.g. [Amazon Cognito](https://aws.amazon.com/cognito/) and [Windows Certificate Store](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores)), and other connection-related features.
Refer to the “[How to setup MQTT5 builder based on desired connection method](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#how-to-create-a-mqtt5-client-based-on-desired-connection-method)” section of the MQTT5 user guide for detailed information and code snippets on each connection type and connection feature.

|Connection Type/Feature	|V1 SDK	|V2 SDK	|User guide section	|	|
|---	|---	|---	|---	|---	|
|	|	|	|	|	|
|MQTT over Secure WebSocket with AWS SigV4 authentication	|✔	|✔	|	|	|
|MQTT with Java Keystore Method	|✔	|✔	|	|X.509	|
|MQTT (over TLS 1.2) with X.509 certificate based mutual authentication	|✘	|✔	|	|X.509	|
|MQTT with PKCS12 Method	|✘	|✔✔*✔****	|	|Container for X.509	|
|MQTT with Custom Key Operation Method	|✔*	|✔	|	|X.509	|
|MQTT with Custom Authorizer Method	|✔*	|✔	|	|	|
|MQTT with Windows Certificate Store Method	|✔*	|✔	|	|X.509	|
|MQTT with PKCS11 Method	|✘	|✔	|	|X.509 plus other formats	|
|Websocket Connection with Cognito Authentication Method	|✘	|✔	|	|	|
|HTTP Proxy	|✔***	|✔	|	|	|

✔* - one option to get this connection type work in V2 SDK, is to [import IOT Core key to a Java KeyStore and convert it to pkcs#12](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/pkcs12_connect.md).
✔** - In order to get this connection type work in V1 SDK, you need to implement the [Custom Authentication workflow](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authorizer.html).
✔*** - Though V1 does not allow to specify HTTP proxy, it is possible to configure systemwide proxy.
✔**** - Available on MacOS only


### Lifecycle Events

Both V1 and V2 SDKs provide lifecycle events for the MQTT clients.

V1 SDK provides 2 lifecycle events: “on Online” and “on Offline”. You can supply a custom callback function via callbacks to `AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient`. It is recommended to use lifecycle events callbacks to help determine the state of the MQTT client during operation.

V2 SDK add 3 new lifecycle events, providing 5 lifecycle events in total: “on connection success”, “on connection failure”, “on disconnect”, “on stopped”, and “on attempting connect”.
Refer to the [MQTT5 user guide](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/documents/MQTT5_Userguide.md#how-to-create-a-mqtt5-client-based-on-desired-connection-method) for the details.

_Example of setting lifecycle events in V1_

```
`def`` myConnectCallback``(``mid``,`` data``):`
`    ``return`

def myDisconnectCallback(mid, data):
    return

client = AWSIoTMQTTClient(clientId)
client.onOnline = on_online_callback
client.onOffline = on_offline_callback

client.configureConnectDisconnectTimeout(10)  # 10 sec
client.connect()

```


_Example of setting lifecycle events in V2_

```
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

V1 SDK provides two API calls for publishing: blocking and non-blocking. For the non-blocking version, the result of the publish operation is reported via a set of callbacks. If you try to publish to a topic that is not allowed by a policy, AWS IoT Core service will close the connection.

V2 SDK provides only asynchronous non-blocking API. [PublishPacketBuilder](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/PublishPacket.PublishPacketBuilder.html) creates a [PublishPacket](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/PublishPacket.html) object containing a description of the PUBLISH packet. The [publish](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/Mqtt5Client.html#publish(software.amazon.awssdk.crt.mqtt5.packets.PublishPacket)) operation takes a `PublishPacket` instance and returns a promise containing a [PublishResult](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/PublishResult.html). The returned `PublishResult` will contain different data depending on the `QoS` used in the publish.

* For QoS 0 (AT_MOST_ONCE): Calling `getValue` will return `null` and the promise will be complete as soon as the packet has been written to the socket.
* For QoS 1 (AT_LEAST_ONCE): Calling `getValue` will return a [PubAckPacket](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/PubAckPacket.html) and the promise will be complete as soon as the PUBACK is received from the broker.

If the operation fails for any reason before these respective completion events, the promise is rejected with a descriptive error. You should always check the reason code of a [PubAckPacket](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/PubAckPacket.html) completion to determine if a QoS 1 publish operation actually succeeded.

_Example of publishing in V1_

```
# Blocking.
client.publish("my/topic", "hello", 0)
```

```
# Non-blocking API.
`client.configureMQTTOperationTimeout`(30) # 30 Seconds
client.connect()

def ack_callback(mid, data=data):
    return

client.publishAsync(
        "my/topic",
        "hello",
        1,
        ackCallback=myPubackCallback)

```

_Example of publishing in V2_

```
publish_future,packet_id = client.publish(mqtt5.PublishPacket(
                                                 topic="my/topic",
                                                 payload=json.dumps("hello"),
                                                 qos=mqtt5.QoS.AT_LEAST_ONCE))
publish_future.result(20) # 20 seconds
```



### Subscribe

V1 provides blocking and non-blocking API for subscribing. To subscribe to topic in V1, you should provide an instance of [AWSIotTopic](http://aws-iot-device-sdk-java-docs.s3-website-us-east-1.amazonaws.com/com/amazonaws/services/iot/client/AWSIotTopic.html) to the [subscribe](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.subscribe) operation. AWSIotTopic object (or, usually, an object of a children class) implements `onMessageReceived` method which will be called on receiving a new message. If you try to subscribe to a topic that is not allowed by a policy, AWS IoT Core service will close the connection.

V2 SDK provides only asynchronous non-blocking API. First, you need to create a [SubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubscribePacket) object. If you specify multiple topics in the *Sequence[*[*Subscription*](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Subscription)*]* parameter, V2 SDK will subscribe to all of these topics using one request. The [subscribe](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.subscribe) operation takes a description of the `SubscribePacket` you wish to send and returns a promise that resolves successfully with the corresponding [SubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubackPacket) returned by the broker; the promise is rejected with an error if anything goes wrong before the `SubAckPacket` is received. You should always check the reason codes of a `SubAckPacket` completion to determine if the subscribe operation actually succeeded.

In V2 SDK, if the MQTT5 client is going to subscribe and receive packets from the MQTT broker, it is important to also setup the `on_publish_callback_fn` callback. This callback is invoked whenever the client receives a message from the server on a topic the client is subscribed to. With this callback, you can process messages made to subscribed topics with its parameter [PublishReceivedData](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishReceivedData).

_Example of subscribing in V1_

```
`client.configureMQTTOperationTimeout(30) # 30 Seconds

def`` ackCallback``(``mid``,`` data``):`
`    ``return`
`    `
`def`` messageCallback``(``client``,`` userdata``,`` message``):`
`    ``return`
`    `
client.subscribe(
        "myTopic/#",
        1,
        ackCallback=mySubackCallback,
        messageCallback=customMessageCallback)

```

_Example of subscribing in V2_

```
subscribe_future = client.subscribe(
        subscribe_packet=mqtt5.SubscribePacket(
                subscriptions=[mqtt5.Subscription(
                topic_filter="my/own/topic",
                qos=mqtt5.QoS.AT_LEAST_ONCE)]))

suback = subscribe_future.result(20)

```



### Unsubscribe

V1 SDK provides blocking and non-blocking API for unsubscribing. To unsubscribe from topic in V1, you should provide a topic string to the [unsubscribe](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html?highlight=unsubscribe#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.unsubscribe) or [unsubscribeAsync](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html?highlight=unsubscribe#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTClient.unsubscribeAsync) operation. The asynchronous operation takes a callback that determines success of failure

V2 SDK provides only asynchronous non-blocking API. First, you need to create an [UnsubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubscribePacket) object.[](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/UnsubscribePacket.UnsubscribePacketBuilder.html) The [unsubscribe](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.unsubscribe) operation takes a description of the [UnsubscribePacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubscribePacket) you wish to send and returns a promise that resolves successfully with the corresponding [UnsubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket) returned by the broker; the promise is rejected with an error if anything goes wrong before the [UnsubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket) is received. You should always check the reason codes of a [UnsubAckPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket) completion to determine if the unsubscribe operation actually succeeded.
Similar to subscribing, you can unsubscribe from multiple topics in one request: just pass a list of topics to topic_filters (*Sequence[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*]) in  *[*UnsubAckPacket*](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.UnsubackPacket)

_Example of unsubscribing in V1_

```
# Blocking API.
client.unsubscribe("my/topic")
client.unsubscribe("another/topic")

```

```
# Non-blocking API.
def unsuback_callback(mid):
    return

client.unsubscribeAsync("my/topic", ackCallback=unsuback_callback)

```


_Example of unsubscribing in V2_

```
unsubscribe_future = mqtt5_client.unsubscribe(
        unsubscribe_packet=mqtt5.UnsubscribePacket(
                topic_filters=["my/topic"]))
unsuback = unsubscribe_future.result(60) # 60 Seconds
print("Unsubscribed with {}".format(unsuback.reason_codes))

```



### Client Stop

In V1 SDK, the `disconnect` method in the `AWSIotMqttClient` class disconnects the client. Once disconnected, the client can connect again by calling `connect`.

In V2 SDK, an MQTT5 client can stop a session by calling the [stop](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.stop) method. You can provide an optional [DisconnectPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectPacket) parameter. A closed client can be started again by calling [start](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.start).

_Example of disconnecting a client in V1_

```
client.disconnect();
```

_Example of disconnecting a client in V2_

```
mqtt5_client.stop(
        disconnect_packet=mqtt5.DisconnectPacket(
                reason_code=mqtt5.*DisconnectReasonCode**.**NORMAL_DISCONNECTION**,
                session_expiry_interval_sec=3600*))

```



### Reconnects

V1 has a maximum number of retry attempts for auto-reconnect. If you exhausted the maximum number of retries, V1 will throw a permanent error and you will not be able to use the same client instance again.

V2 attempts to reconnect automatically until connection succeeds or `client.stop()` is called. The reconnection parameters, such as min/max delays and [jitter modes](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ExponentialBackoffJitterMode), are configurable through [awsiot.mqtt5_client_builder](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt5_client_builder.html#module-awsiot.mqtt5_client_builder).


_Example of tweaking reconnection settings in V1_

```
*`baseReconnectQuietTimeSecond`*` ``=`` ``1 # Initial backoff time`
`maxReconnectQuiteTimeSecond ``=`` ``23 # maximum backoff time`
`stableConnectionTimeSecond ``=`` ``20  # the time the connection is considered stable`
`client``.``configureAutoReconnectBackoffTime``(
        ``baseReconnectQuietTimeSecond``,
        ``maxReconnectQuiteTimeSecond``,
        ``stableConnectionTimeSecond``)

`
```

_Example of tweaking reconnection settings in V2_

```
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

In V1, if you’re having too many in-flight QoS 1 messages, you can encounter the `too many publishes in Progress` error on publishing messages. This is caused by the so-called in-flight publish limit. By default, V1 SDK supports a maximum of 20 in-flight operations.

V2 does not limit the number of in-flight messages. Additionally, V2 provides a way to configure which kind of packets will be placed into the offline queue when the client is in the disconnected state. The following code snippet demonstrates how to enable storing all packets except QOS0 publish packets in the offline queue on disconnect:

_Example of configuring the offline queue in V2_

```
mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
 ...
        offline_queue_behavior=
            mqtt5.ClientOperationQueueBehaviorType.FAIL_QOS0_PUBLISH_ON_DISCONNECT)

mqtt5_client.start()
```

Note that AWS IoT Core [limits the number of allowed operations per second](https://docs.aws.amazon.com/general/latest/gr/iot-core.html#message-broker-limits). The [get_stats](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.get_stats) method returns  the current state of an `awscrt.mqtt5.Client` object’s queue of operations in [OperationStatisticsData](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.OperationStatisticsData), which may help with tracking the number of in-flight messages.

```
op_stats_data = mqtt5_client.get_stats()
print(
    "Client operations queue statistics:\n" +
    "incomplete_operation_count:" + op_stats_data.incomplete_operation_count() + "\n"
    "incomplete_operation_size: " + op_stats_data.incomplete_operation_size() + "\n"
    "unacked_operation_count: " + op_stats_data.unacked_operation_count() + "\n"
    "unacked_operation_size: " + op_stats_data.unacked_operation_size() + "\n")

```

See [withOfflineQueueBehavior documentation](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions) for more details.
See [ClientOfflineQueueBehavior types documentation](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOperationQueueBehaviorType) to find the list of the supported offline queue behaviors and their description.


### Operation Timeouts

In V1 SDK, all operations (*publish*, *subscribe*, *unsubscribe*) will not timeout unless you define a timeout for them. If no timeout is defined, there is a possibility that an operation will wait forever for the server to respond and block the calling thread indefinitely.

In V2 SDK, operations timeout is set for the MQTT5 client with the [ClientOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions) class member `ack_timeout_sec`. The default value is no timeout. As in V1 SDK, failing to set a timeout can cause an operation to stuck forever, but it won’t block the client.
The [get_stats](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client.get_stats) method returns  the current state of an` mqtt5.Client` object’s queue of operations, which may help with tracking operations.

_Example of timeouts in V1_

```
connectTimeoutSec = 10
`client``.``configureConnectDisconnectTimeout`(connectTimeoutSec)
client.connect();

 publishTimeoutMs = 20
client.`configureMQTTOperationTimeout``(publishTimeoutMs)`
client.publish("my/topic", "hello", 1)

```

_Example of timeouts in V2_

```
mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint="<prefix>-ats.iot.<region>.amazonaws.com",
        cert_filepath="<certificate file path>",
        pri_key_filepath="<private key file path>",
        ack_timeout_sec=20
)
```



### Logging

V1 SDK uses `AWSIoTPythonSDK.core` custom logger logger for logging.

V2 SDK uses a standard  [logging facility](https://docs.python.org/3/howto/logging.html).

_Example of using logging in V1_

```
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.error("error log")
logger.info("info log")
```

_Example of using logging in V2_

```
from awscrt import io
import logging

io.init_logging(log_level=io.LogLevel.Trace, file_name='stderr')

logger.debug("error log")

```



### Client for Device Shadow Service

V1 SDK is built with [AWS IoT device shadow support](http://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-shadows.html), providing access to thing shadows (sometimes referred to as device shadows). It also supports a simplified shadow access model, which allows developers to exchange data with their shadows by just using getter and setter methods without having to serialize or deserialize any JSON documents.

V2 SDK supports device shadow service as well, but with completely different API.
First, you subscribe to special topics to get data and feedback from a service. The service client provides API for that. For example, `subscribe_to_get_shadow_accepted`  subscribes to a topic to which AWS IoT Core will publish a shadow document; and via the `subscribe_to_get_shadow_rejected` the server will notify you if it cannot send you a requested document.
After subscribing to all the required topics, the service client can start interacting with the server, for example update the status or request for data. These actions are also performed via client API calls. For example, `publish_get_shadow`  sends a request to AWS IoT Core to get a shadow document. The requested Shadow document will be received in a callback specified in the `subscribe_to_get_shadow_accepted` call.

AWS IoT Core [documentation for Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html) service provides detailed descriptions for the topics used to interact with the service.

_Example of creating a Device Shadow service client in V1_

```
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

_Example of creating a Device Shadow service client in V2_

```
mqtt5_client.start()
shadow_client = iotshadow.IotShadowClient(mqtt5_client)
```

_Example of deleting a Device Shadow in V1_

```
# Delete Shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    return
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

```

_Example of deleting a Classic Shadow in V2_

```
def delete_accepted(DeleteShadowResponse response):
    return
shadow_client.subscribe_to_delete_shadow_accepted(*request*, *qos*, *callback*)

def delete_rejected(DeleteShadowResponse response):
    return
shadow_client.subscribe_to_delete_shadow_rejected(*request*, *qos*, *callback*)

iotshadow.DeleteShadowRequest req
req.client_token = "<client token>"
req.thing_name = "<thing name>"

shadow_future = shadow_client.publish_delete_shadow(
        request=req,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

```

_Example of updating a Classic Shadow in V1_

```
# Update Shadow
def customShadowCallback_Update(payload, responseStatus, token):
    return

JSONPayload = '{"state":{"desired":{"property":' + str(3) + '}}}'
deviceShadowHandler.shadowUpdate(
        JSONPayload,
        customShadowCallback_Update,
        5)

```

_Example of updating a Classic Shadow in V2_

```
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

_Example of subscribing to a delta Shadow events in V1_

```
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

_Example of subscribing to a delta Shadow events in V2_

```
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


See API documentation for V2 SDK [Device Shadow](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotshadow.html) service client for more details.
Refer to the V2 SDK [Device Shadow](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/shadow_mqtt5.py) sample for code example.


### Client for Jobs Service

V1 and V2 SDK offer support of AWS IoT Core services implementing a service client for the [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) service which helps with defining a set of remote operations that can be sent to and run on one or more devices connected to AWS IoT.
V1 IotJobs APIs are defined [here](https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html#AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTThingJobsClient), with its corresponding code [samples](https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/jobs/jobsSample.py)

V2 SDK supports Jobs service as well, but with completely different API.
The Jobs service client provides API similar to API provided by [Client for Device Shadow Service](https://quip-amazon.com/RUfpAM2x5mXr#temp:C:XVAbbb7cff5d5884fdfb4dcf670f). First, you subscribe to special topics to get data and feedback from a service. The service client provides API for that. After subscribing to all the required topics, the service client can start interacting with the server, for example update the status or request for data. These actions are also performed via client API calls.

AWS IoT Core documentation for [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/jobs-mqtt-api.html) service provides detailed descriptions for the topics used to interact with the service.

See API documentation for V2 SDK [Jobs](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotjobs.html) service clients for more details.
Refer to the V2 SDK [Jobs](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/jobs_mqtt5.py) samples for code examples.

_V1 Jobs Example_

```
jobs_client = AWSIoTMQTTThingJobsClient(
        "<client id>",
        "<thing name>",
        QoS=1,
        awsIoTMQTTClient=mqtt5_client)

jobsClient.connect()

# Setup Callbacks
def newJobReceived(self, mqtt5_client, userdata, message):
    return
jobs_client.createJobSubscription(
        newJobReceived,
        jobExecutionTopicType.
        JOB_NOTIFY_NEXT_TOPIC)

def startNextJobSuccessfullyInProgress(mqtt5_client, userdata, message):
    return
jobs_client.createJobSubscription(
        startNextJobSuccessfullyInProgress,
        jobExecutionTopicType.JOB_START_NEXT_TOPIC,
        jobExecutionTopicReplyType.JOB_ACCEPTED_REPLY_TYPE)

def startNextRejected(mqtt5_client, userdata, message):
    return
jobs_client.createJobSubscription(
        startNextRejected,
        jobExecutionTopicType.JOB_START_NEXT_TOPIC,
        jobExecutionTopicReplyType.JOB_REJECTED_REPLY_TYPE)

def updateJobSuccessful(mqtt5_client, userdata, message):
    return
jobs_client.createJobSubscription(
        updateJobSuccessful,
        jobExecutionTopicType.JOB_UPDATE_TOPIC,
        jobExecutionTopicReplyType.JOB_ACCEPTED_REPLY_TYPE,
        '+')

def updateJobRejected(mqtt5_client, userdata, message):
    return
jobs_client.createJobSubscription(
        updateJobRejected,
        jobExecutionTopicType.JOB_UPDATE_TOPIC,
        jobExecutionTopicReplyType.JOB_REJECTED_REPLY_TYPE,
        '+')

# start next job
statusDetails =
        {'StartedBy': 'ClientToken: {} on {}'.format(
                clientToken,
                datetime.datetime.now().isoformat())}

jobs_client.sendJobsStartNext(
                 statusDetails=statusDetails)

# Update job status
jobs_cli.`sendJobsUpdate(
        jobId="<job id>",
        statusDetails=None,
        `expectedersion=4,
        executionNumber=3,
        includeJobExecutionState=False,
        includeJobDocument=False
        stepTimeoutInMinutes=3)

jobsClient.disconnect()

```


_V2 Jobs example_

```
jobs_client = iotjobs.IotJobsClient(mqtt5_client)
get_jobs_request = iotjobs.GetPendingJobExecutionsRequest(thing_name="<thing name">)

# List pending jobs
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

get_jobs_request_future = jobs_client.publish_get_pending_job_executions(
        request=get_jobs_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE)

# Subscribe to necessary topics
changed_subscription_request = iotjobs.NextJobExecutionChangedSubscriptionRequest(
        thing_name="<thing name>")

def on_next_job_execution_changed(event):
    return
subscribed_future, _ = jobs_client.subscribe_to_next_job_execution_changed_events(
        request=changed_subscription_request,
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        callback=on_next_job_execution_changed)

start_subscription_request = iotjobs.StartNextPendingJobExecutionSubscriptionRequest(
        thing_name="<thing name>")

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

# Note that we subscribe to "+", the MQTT wildcard, to receive
# responses about any job-ID.
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

# Start next Job
request = iotjobs.StartNextPendingJobExecutionRequest(
        thing_name="<thing name">)
publish_future = jobs_client.publish_start_next_pending_job_execution(
        request,
        mqtt5.QoS.AT_LEAST_ONCE)
publish_future.add_done_callback(
        on_publish_start_next_pending_job_execution)

```



### Client for Fleet Provisioning Service

Another IoT service that V2 SDK provides access to is [Fleet Provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html) (also known as Identity Service). By using AWS IoT fleet provisioning, AWS IoT can generate and securely deliver device certificates and private keys to your devices when they connect to AWS IoT for the first time.

The Fleet Provisioning service client provides API similar to API provided by [Client for Device Shadow Service](https://quip-amazon.com/RUfpAM2x5mXr#temp:C:XVAbbb7cff5d5884fdfb4dcf670f). First, you subscribe to special topics to get data and feedback from a service. The service client provides API for that. After subscribing to all the required topics, the service client can start interacting with the server, for example update the status or request for data. These actions are also performed via client API calls.

AWS IoT Core documentation for [Fleet Provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html) service provides detailed descriptions for the topics used to interact with the service.

See API documentation for V2 SDK  [Fleet Provisioning](https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/iotidentity.html) service client for more details.
Refer to the V2 SDK [Fleet Provisioning](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/fleetprovisioning.md) samples for code examples.


### Example

It’s always helpful to look at a working example to see how new functionality works, to be able to tweak different options, to compare with existing code. For that reasons, we implemented a [Publish/Subscribe example](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt5_pubsub.md) ([source code](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt5_pubsub.py)) in V2 SDK similar to a sample provided by V1 SDK (see a corresponding [readme section](https://github.com/aws/aws-iot-device-sdk-python/blob/master/README.rst#basicpubsub) and [source code](https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py)).

## How to get help

For any migration related questions or feedback, you can contact us at [discussion](https://github.com/aws/aws-iot-device-sdk-python-v2/discussions) by submitting an issue with a label `label:migration`.

## Appendix

### MQTT5 Features

**Clean Start and Session Expiry**
You can use Clean Start and Session Expiry to handle your persistent sessions with more flexibility.
Refer to [awscrt.mqtt5.ClientSessionBehaviorType](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientSessionBehaviorType) enum and [NegotiatedSettings.session_expiry_interval_sec](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.NegotiatedSettings) method for details.

**Reason Code on all ACKs**
You can debug or process error messages more easily using the reason codes. Reason codes are returned by the message broker based on the type of interaction with the broker (Subscribe, Publish, Acknowledge).
See [PubAckReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PubackReasonCode), [SubAckReasonCode](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/SubAckPacket.SubAckReasonCode.html), [UnsubAckReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.SubackReasonCode), [ConnectReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnectReasonCode), [DisconnectReasonCode](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectReasonCode). 

**Topic Aliases**
You can substitute a topic name with a topic alias, which is a two-byte integer.
Use [mqtt5.TopicAliasingOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.TopicAliasingOptions) with [mqtt5.ClientOptions](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOptions), and when creating a [PUBLISH packet](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) use the parameter topic_alias(int).

**Message Expiry**
You can add message expiry values to published messages. Use [message_expiry_interval_sec](https://awslabs.github.io/aws-crt-java/software/amazon/awssdk/crt/mqtt5/packets/PublishPacket.PublishPacketBuilder.html#withMessageExpiryIntervalSeconds(java.lang.Long)) variable when creating a [PUBLISH packet](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket).

**Server disconnect**
When a disconnection happens, the server can proactively send the client a DISCONNECT to notify connection closure with a reason code for disconnection.
Refer to [DisconnectPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.DisconnectPacket) class for details.

**Request/Response**
Publishers can request a response be sent by the receiver to a publisher-specified topic upon reception. Use `response_topic` method in [PublishPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) class.

**Maximum Packet Size**
Client and Server can independently specify the maximum packet size that they support. See [ConnectPacket.maximum_packet_size(int)](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnectPacket), [NegotiatedSettings.maximum_packet_size_to_server](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.NegotiatedSettings), and [ConnAckPacket.maximum_packet_size](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ConnackPacket) methods.

**Payload format and content type**
You can specify the payload format (binary, text) and content type when a message is published. These are forwarded to the receiver of the message. Use content_type(str) method in [PublishPacket](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.PublishPacket) class.

**Shared Subscriptions**
Shared Subscriptions allow multiple clients to share a subscription to a topic and only one client will receive messages published to that topic using a random distribution.
Refer to a [shared subscription sample](https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/mqtt5_shared_subscription.md) in V2 SDK.
**NOTE** AWS IoT Core provides this functionality for MQTT3 as well.

