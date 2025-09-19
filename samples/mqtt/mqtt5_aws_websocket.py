# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, auth
import threading, time

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

parser = argparse.ArgumentParser(
    description="MQTT5 AWS Websocket Sample.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required Arguments
required.add_argument("--endpoint", required=True,  metavar="", dest="input_endpoint",
                      help="IoT endpoint hostname")
required.add_argument("--signing_region", required=True,  metavar="", dest="input_signing_region",
                      help="Signing region for websocket connection")

# Optional Arguments
optional.add_argument("--client_id",  metavar="", dest="input_clientId", default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}",
                      help="Client ID")
optional.add_argument("--topic", default="test/topic",  metavar="", dest="input_topic",
                      help="Topic")
optional.add_argument("--message", default="Hello from mqtt5 sample",  metavar="", dest="input_message",
                      help="Message payload")
optional.add_argument("--count", type=int, default=5,  metavar="", dest="input_count",
                      help="Messages to publish (0 = infinite)")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------

TIMEOUT = 100
message_count = args.input_count
message_topic = args.input_topic
message_string = args.input_message
# Events used within callbacks to progress sample
connection_success_event = threading.Event()
stopped_event = threading.Event()
received_all_event = threading.Event()
received_count = 0


# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    print("==== Received message from topic '{}': {} ====\n".format(
        publish_packet.topic, publish_packet.payload.decode('utf-8')))

    # Track number of publishes received
    global received_count
    received_count += 1
    if received_count == args.input_count:
        received_all_event.set()


# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped\n")
    stopped_event.set()


# Callback for lifecycle event Attempting Connect
def on_lifecycle_attempting_connect(lifecycle_attempting_connect_data: mqtt5.LifecycleAttemptingConnectData):
    print("Lifecycle Connection Attempt\nConnecting to endpoint: '{}' with client ID'{}'".format(
        args.input_endpoint, args.input_clientId))


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    connack_packet = lifecycle_connect_success_data.connack_packet
    print("Lifecycle Connection Success with reason code:{}\n".format(
        repr(connack_packet.reason_code)))
    connection_success_event.set()


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure with exception:{}".format(
        lifecycle_connection_failure.exception))


# Callback for the lifecycle event Disconnection
def on_lifecycle_disconnection(lifecycle_disconnect_data: mqtt5.LifecycleDisconnectData):
    print("Lifecycle Disconnected with reason code:{}".format(
        lifecycle_disconnect_data.disconnect_packet.reason_code if lifecycle_disconnect_data.disconnect_packet else "None"))


if __name__ == '__main__':
    print("\nStarting MQTT5 Websocket Sample\n")
    message_count = args.input_count
    message_topic = args.input_topic
    message_string = args.input_message

    # Create a default AWS credentials provider which uses the provider chain used by most AWS SDKs
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain()

    # Create MQTT5 client that uses a credentials provider to sign the websocket handshake
    print("==== Creating MQTT5 Client ====\n")
    client = mqtt5_client_builder.websockets_with_default_aws_signing(
        endpoint=args.input_endpoint,
        region=args.input_signing_region,
        credentials_provider=credentials_provider,
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        on_lifecycle_disconnection=on_lifecycle_disconnection,
        client_id=args.input_clientId)
    

    # Start the client, instructing the client to desire a connected state. The client will try to 
    # establish a connection with the provided settings. If the client is disconnected while in this 
    # state it will attempt to reconnect automatically.
    print("==== Starting client ====")
    client.start()

    # We await the `on_lifecycle_connection_success` callback to be invoked.
    if not connection_success_event.wait(TIMEOUT):
        raise TimeoutError("Connection timeout")


    # Subscribe 
    print("==== Subscribing to topic '{}' ====".format(message_topic))
    subscribe_future = client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
        subscriptions=[mqtt5.Subscription(
            topic_filter=message_topic,
            qos=mqtt5.QoS.AT_LEAST_ONCE)]
    ))
    suback = subscribe_future.result(TIMEOUT)
    print("Suback received with reason code:{}\n".format(suback.reason_codes))


    # Publish
    if message_count == 0:
        print("==== Sending messages until program killed ====\n")
    else:
        print("==== Sending {} message(s) ====\n".format(message_count))

    publish_count = 1
    while (publish_count <= message_count) or (message_count == 0):
        message = f"{message_string} [{publish_count}]"
        print(f"Publishing message to topic '{message_topic}': {message}")
        publish_future = client.publish(mqtt5.PublishPacket(
            topic=message_topic,
            payload=message,
            qos=mqtt5.QoS.AT_LEAST_ONCE
        ))
        publish_completion_data = publish_future.result(TIMEOUT)
        print("PubAck received with {}\n".format(repr(publish_completion_data.puback.reason_code)))
        time.sleep(1.5)
        publish_count += 1

    received_all_event.wait(TIMEOUT)
    print("{} message(s) received.\n".format(received_count))

    # Unsubscribe
    print("==== Unsubscribing from topic '{}' ====".format(message_topic))
    unsubscribe_future = client.unsubscribe(unsubscribe_packet=mqtt5.UnsubscribePacket(
        topic_filters=[message_topic]))
    unsuback = unsubscribe_future.result(TIMEOUT)
    print("Unsubscribed with {}\n".format(unsuback.reason_codes))


    # Stop the client. Instructs the client to disconnect and remain in a disconnected state.
    print("==== Stopping Client ====")
    client.stop()

    if not stopped_event.wait(TIMEOUT):
        raise TimeoutError("Stop timeout")

    print("==== Client Stopped! ====")
