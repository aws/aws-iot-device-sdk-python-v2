# MQTT 5
## Developer Preview Disclaimer
MQTT5 support is currently in **developer preview**.  We encourage feedback at all times, but feedback during the preview window is especially valuable in shaping the final product.  During the preview period we may make backwards-incompatible changes to the public API, but in general, this is something we will try our best to avoid.

The MQTT5 client cannot yet be used with the AWS IoT MQTT services (Shadow, Jobs, Identity).  This is a shortcoming that we hope to address in the near future.

## Introduction

This user guide is designed to act as a reference and guide for how to use MQTT5 with the Java SDK. This guide includes code snippets for how to make a MQTT5 client with proper configuration, how to connect to AWS IoT Core, how to perform operations and interact with AWS IoT Core through MQTT5, and some best practices for MQTT5.

If you are completely new to MQTT, it is highly recommended to check out the following resources to learn more about MQTT:

* MQTT.org getting started: https://mqtt.org/getting-started/
* MQTT.org FAQ (includes list of commonly used terms): https://mqtt.org/faq/
* MQTT on AWS IoT Core documentation: https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html
* MQTT 5 standard: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html
* MQTT 311 standard: https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html

This user guide expects some beginner level familiarity with MQTT and the terms used to describe MQTT.

## What's Different? (relative to the MQTT311 implementation)
SDK MQTT5 support comes from a separate client implementation.  In doing so, we took the opportunity to incorporate feedback about the 311 client that we could not apply without making breaking changes.  If you're used to the 311 client's API contract, there are a number of differences.

### Major changes
* The MQTT5 client does not treat initial connection failures differently.  With the 311 implementation, a failure during initial connect would halt reconnects completely.
* The set of client lifecycle events is expanded and contains more detailed information whenever possible.  All protocol data is exposed to the user.
* MQTT operations are completed with the full associated ACK packet when possible.
* New behavioral configuration options:
    * [IoT Core specific validation](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ExtendedValidationAndFlowControlOptions) - will validate and fail operations that break IoT Core specific restrictions
    * [IoT Core specific flow control](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ExtendedValidationAndFlowControlOptions) - will apply flow control to honor IoT Core specific per-connection limits and quotas
    * [Flexible queue control](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.ClientOperationQueueBehaviorType) - provides a number of options to control what happens to incomplete operations on a disconnection event
* A [new API](https://awslabs.github.io/aws-crt-python/api/mqtt5.html#awscrt.mqtt5.Client) has been added to query the internal state of the client's operation queue.  This API allows the user to make more informed flow control decisions before submitting operatons to the client.
* Data can no longer back up on the socket.  At most one frame of data is ever pending-write on the socket.
* The MQTT5 client has a single message-received callback.  Per-subscription callbacks are not supported.

### Minor changes
* Public API terminology has changed.  You `start()` or `stop()` the MQTT5 client.  This removes the semantic confusion with connect/disconnect as client-level controls vs. internal recurrent networking events.
* With the 311 implementation, there were two separate objects, a client and a connection.  With MQTT5, there is only the client.

### Not Supported
Not all parts of the MQTT5 spec are supported by the implementation.  We currently do not support:
* AUTH packets and the authentication fields in the CONNECT packet
* QoS 2

## Client lifecycle management
Once created, an MQTT5 client's configuration is immutable.  Invoking start() on the client will put it into an active state where it
recurrently establishes a connection to the configured remote endpoint.  Reconnecting continues until you invoke stop().

```
# Create an MQTT5 Client

    client_options = mqtt5.ClientOptions(
        host_name = <endpoint to connect to>,
        port = <port to use>)

    # Other options in client options can be set but once Client is initialized configuration is immutable
    # e.g. setting the on_publish_callback_fn to be called
    # client_options.on_publish_callback_fn = on_publish_received

    client = mqtt5.Client(client_options)


# Use the client
    client.start();
    ...
```

Invoking stop() breaks the current connection (if any) and moves the client into an idle state.

```
    // Shutdown
    client.stop();

```

## Connecting To AWS IoT Core
We strongly recommend using the AwsIotMqtt5ClientConfigBuilder class to configure MQTT5 clients when connecting to AWS IoT Core.  The builder simplifies configuration for all authentication methods supported by AWS IoT Core.  This section shows samples for all of the authentication possibilities.

#### **Direct MQTT with X509-based mutual TLS**
For X509 based mutual TLS, you can create a client where the certificate and private key are configured by path:
```
    # X.509 based certificate file
    certificate_file_path = "<certificate file path>"
    # PKCS#1 or PKCS#8 PEM encoded private key file
    private_key_filePath = "<private key file path>"

    # other builder configurations can be added using **kwargs in the builder

    # Create an MQTT5 Client using mqtt5_client_builder
    client = mqtt5_client_builder.mtls_from_path(
        endpoint = <account-specific endpoint>,
        cert_filepath=certificate_file_path,
        pri_key_filepath=private_key_filePath))
```

#### **MQTT over Websockets with Sigv4 authentication**
Sigv4-based authentication requires a credentials provider capable of sourcing valid AWS credentials. Sourced credentials
will sign the websocket upgrade request made by the client while connecting.  The default credentials provider chain supported by
the SDK is capable of resolving credentials in a variety of environments according to a chain of priorities:

```Environment -> Profile (local file system) -> STS Web Identity -> IMDS (ec2) or ECS```
If the default credentials provider chain and built-in AWS region extraction logic are sufficient, you do not need to specify
any additional configuration:
```
    # The signing region. e.x.: 'us-east-1'
    signing_region = <signing region>
    credentials_provider = auth.AwsCredentialsProvider.new_dfault_chain()

    # other builder configurations can be added using **kwargs in the builder

    # Create an MQTT5 Client using mqtt5_client_builder
    client = mqtt5_client_builder.websockets_with_default_aws_signing(
        endpoint = <account-specific endpoint>,
        region = signing_region,
        credentials_provider=credentials_provider))
```

#### **Direct MQTT with Custom Authentication**
AWS IoT Core Custom Authentication allows you to use a lambda to gate access to IoT Core resources.  For this authentication method,
you must supply an additional configuration structure containing fields relevant to AWS IoT Core Custom Authentication.
If your custom authenticator does not use signing, you don't specify anything related to the token signature:
```
    # other builder configurations can be added using **kwargs in the builder

    client = mqtt5_client_builder.direct_with_custom_authorizer(
        endpoint = <account-specific endpoint>,
        auth_authorizer_name = <Name of your custom authorizer>,
        auth_username = <Value of the username field that should be passed to the authorizer's lambda>,
        auth_password =<Binary data value of the password field that should be passed to the authorizer's lambda>)
```
If your custom authorizer uses signing, you must specify the three signed token properties as well.  The token signature must be the URI-encoding of the base64 encoding of the digital signature of the token value via the private key associated with the public key that was registered with the custom authorizer.  It is your responsibility to URI-encode the token signature.
```
    # other builder configurations can be added using **kwargs in the builder

    client = mqtt5_client_builder.direct_with_custom_authorizer(
        endpoint = <account-specific endpoint>,
        auth_authorizer_name = <Name of your custom authorizer>,
        auth_username = <Value of the username field that should be passed to the authorizer's lambda>,
        auth_password =<Binary data value of the password field that should be passed to the authorizer's lambda>,
        auth_authorizer_signature=<The signature of the custom authorizer>)
```
In both cases, the builder will construct a final CONNECT packet username field value for you based on the values configured.  Do not add the token-signing fields to the value of the username that you assign within the custom authentication config structure.  Similarly, do not add any custom authentication related values to the username in the CONNECT configuration optionally attached to the client configuration. The builder will do everything for you.

#### **HTTP Proxy**
No matter what your connection transport or authentication method is, you may connect through an HTTP proxy
by adding the http_proxy_options keyword argument to the builder:
```
    http_proxy_options = http.HttpProxyOptions(
        host_name = <proxy host>,
        port = <proxy port>)

    # Create an MQTT5 Client using mqtt5_client_builder with proxy options as keyword argument
    client = mqtt5_client_builder.mtls_from_path(
        endpoint = <account-specific endpoint>,
        cert_filepath = <certificate file path>,
        pri_key_filepath = <private key file path>,
        http_proxy_options = http_proxy_options))
```
SDK Proxy support also includes support for basic authentication and TLS-to-proxy.  SDK proxy support does not include any additional
proxy authentication methods (kerberos, NTLM, etc...) nor does it include non-HTTP proxies (SOCKS5, for example).

## Lifecycle Events
The MQTT5 client emits a set of events related to state and network status changes.

#### **AttemptingConnect**
Emitted when the client begins to make a connection attempt.

#### **ConnectionSuccess**
Emitted when a connection attempt succeeds based on receipt of an affirmative CONNACK packet from the MQTT broker.  A ConnectionSuccess event includes the MQTT broker's CONNACK packet, as well as a structure -- the NegotiatedSettings -- which contains the final values for all variable MQTT session settings (based on protocol defaults, client wishes, and server response).

#### **ConnectionFailure**
Emitted when a connection attempt fails at any point between DNS resolution and CONNACK receipt.  In addition to an error code, additional data may be present in the event based on the context.  For example, if the remote endpoint sent a CONNACK with a failing reason code, the CONNACK packet will be included in the event data.

#### **Disconnect**
Emitted when the client's network connection is shut down, either by a local action, event, or a remote close or reset.  Only emitted after a ConnectionSuccess event: a network connection that is shut down during the connecting process manifests as a ConnectionFailure event.  A Disconnect event will always include an error code.  If the Disconnect event is due to the receipt of a server-sent DISCONNECT packet, the packet will be included with the event data.

#### **Stopped**
Emitted once the client has shutdown any associated network connection and entered an idle state where it will no longer attempt to reconnect.  Only emitted after an invocation of stop() on the client.  A stopped client may always be started again.

## Client Operations
There are four basic MQTT operations you can perform with the MQTT5 client.

### Subscribe
The Subscribe operation takes a description of the SUBSCRIBE packet you wish to send and returns a future that resolves successfully with the corresponding SUBACK returned by the broker; the future result raises an exception if anything goes wrong before the SUBACK is received.
```
    subscribe_future = client.subscribe(subscribe_packet = mqtt5.SubscribePacket(
        subscriptions = [mqtt5.Subscription(
            topic_filter = "hello/world/qos1",
            qos = mqtt5.QoS.AT_LEAST_ONCE)]))

    suback = subscribe_future.result()
```
### Unsubscribe
The Unsubscribe operation takes a description of the UNSUBSCRIBE packet you wish to send and returns a future that resolves successfully with the corresponding UNSUBACK returned by the broker; the future result raises an exception if anything goes wrong before the UNSUBACK is received.
```
    unsubscribe_future = client.unsubscribe(unsubscribe_packet = mqtt5.UnsubscribePacket(
        topic_filters=["hello/world/qos1"]))

    unsuback = unsubscribe_future.result()
```
### Publish
The Publish operation takes a description of the PUBLISH packet you wish to send and returns a future of polymorphic value.  If the PUBLISH was a QoS 0 publish, then the future result is an empty PUBACK packet with all members set to None and is completed as soon as the packet has been written to the socket.  If the PUBLISH was a QoS 1 publish, then the future result is a PUBACK packet value and is completed as soon as the PUBACK is received from the broker.  If the operation fails for any reason before these respective completion events, the future result raises an exception.
```
    publish_future = client.publish(mqtt5.PublishPacket(
        topic = "hello/world/qos1",
        payload = "This is the payload of a QoS 1 publish",
        qos = mqtt5.QoS.AT_LEAST_ONCE))

    # on success, the result of publish_future will be a PubackPacket
    puback = publish_future.result()
```
### Disconnect
The stop() API supports a DISCONNECT packet as an optional parameter.  If supplied, the DISCONNECT packet will be sent to the server prior to closing the socket.  There is no future returned by a call to stop() but you may listen for the 'stopped' event on the client.
```
    client.stop(mqtt5.DisconnectPacket(
        reason_code = mqtt5.DisconnectReasonCode.NORMAL_DISCONNECTION,
        session_expiry_interval_sec = 3600))
```