# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, http
import threading, time, json
from concurrent.futures import Future

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

parser = argparse.ArgumentParser(
    description="MQTT5 pub/sub Sample (mTLS).",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
# Connection / TLS
parser.add_argument("--endpoint", required=True, dest="input_endpoint", help="IoT endpoint hostname")
parser.add_argument("--port", type=int, default=8883, dest="input_port", help="Port (8883 mTLS, 443 ALPN)")
parser.add_argument("--cert", required=True, dest="input_cert",
                    help="Path to the certificate file to use during mTLS connection establishment")
parser.add_argument("--key", required=True, dest="input_key",
                    help="Path to the private key file to use during mTLS connection establishment")
parser.add_argument("--ca_file", dest="input_ca", help="Path to optional CA bundle (PEM)")
# Messaging
parser.add_argument("--topic", default="test/topic", dest="input_topic", help="Topic")
parser.add_argument("--message", default="Hello from mqtt5 sample", dest="input_message", help="Message payload")
parser.add_argument("--count", type=int, default=5, dest="input_count",
                    help="Messages to publish (0 = infinite)")
# Proxy
parser.add_argument("--proxy-host", dest="input_proxy_host", help="HTTP proxy host")
parser.add_argument("--proxy-port", type=int, default=0, dest="input_proxy_port", help="HTTP proxy port")
# Misc
parser.add_argument("--client-id", dest="input_clientId",
                    default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}", help="Client ID")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


TIMEOUT = 100
topic_filter = "test/topic"

received_count = 0
received_all_event = threading.Event()
future_stopped = Future()
future_connection_success = Future()

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))
    global received_count
    received_count += 1
    if received_count == args.input_count:
        received_all_event.set()


# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure")
    print("Connection failed with exception:{}".format(lifecycle_connection_failure.exception))


if __name__ == '__main__':
    print("\nStarting MQTT5 PubSub Sample\n")
    message_count = int(args.input_count)
    message_topic = args.input_topic
    message_string = args.input_message

    # Create the proxy options if the data is present in args
    proxy_options = None
    if args.input_proxy_host is not None and args.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=args.input_proxy_host,
            port=args.input_proxy_port)

    # Create MQTT5 client
    client = mqtt5_client_builder.mtls_from_path(
        endpoint=args.input_endpoint,
        port=args.input_port,
        cert_filepath=args.input_cert,
        pri_key_filepath=args.input_key,
        ca_filepath=args.input_ca,
        http_proxy_options=proxy_options,
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        client_id=args.input_clientId)
    print("MQTT5 Client Created")

    
    print("Connecting to endpoint with client ID")

    client.start()
    lifecycle_connect_success_data = future_connection_success.result(TIMEOUT)
    connack_packet = lifecycle_connect_success_data.connack_packet
    negotiated_settings = lifecycle_connect_success_data.negotiated_settings
    print(f"Connected to endpoint:'{args.input_endpoint}' with Client ID:'{args.input_clientId}' with reason_code:{repr(connack_packet.reason_code)}")

    # Subscribe

    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future = client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
        subscriptions=[mqtt5.Subscription(
            topic_filter=message_topic,
            qos=mqtt5.QoS.AT_LEAST_ONCE)]
    ))
    suback = subscribe_future.result(TIMEOUT)
    print("Subscribed with {}".format(suback.reason_codes))

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    if message_string:
        if message_count == 0:
            print("Sending messages until program killed")
        else:
            print("Sending {} message(s)".format(message_count))

        publish_count = 1
        while (publish_count <= message_count) or (message_count == 0):
            message = "{} [{}]".format(message_string, publish_count)
            print("Publishing message to topic '{}': {}".format(message_topic, message))
            publish_future = client.publish(mqtt5.PublishPacket(
                topic=message_topic,
                payload=json.dumps(message_string),
                qos=mqtt5.QoS.AT_LEAST_ONCE
            ))

            publish_completion_data = publish_future.result(TIMEOUT)
            print("PubAck received with {}".format(repr(publish_completion_data.puback.reason_code)))
            time.sleep(1)
            publish_count += 1

    received_all_event.wait(TIMEOUT)
    print("{} message(s) received.".format(received_count))

    # Unsubscribe

    print("Unsubscribing from topic '{}'".format(message_topic))
    unsubscribe_future = client.unsubscribe(unsubscribe_packet=mqtt5.UnsubscribePacket(
        topic_filters=[message_topic]))
    unsuback = unsubscribe_future.result(TIMEOUT)
    print("Unsubscribed with {}".format(unsuback.reason_codes))

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
