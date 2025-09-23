# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse
import uuid

parser = argparse.ArgumentParser(
    description="PubSub Sample (MQTT3)",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required Arguments
required.add_argument("--endpoint", required=True, metavar="", dest="input_endpoint",
                      help="IoT endpoint hostname")
required.add_argument("--cert", required=True, metavar="", dest="input_cert",
                      help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument("--key", required=True, metavar="", dest="input_key",
                      help="Path to the private key file to use during mTLS connection establishment")

# Optional Arguments
optional.add_argument("--client_id", metavar="", dest="input_clientId", default=f"pubsub-sample-{uuid.uuid4().hex[:8]}",
                      help="Client ID")
optional.add_argument("--topic", metavar="", default="test/topic", dest="input_topic",
                      help="Topic")
optional.add_argument("--message", metavar="", default="Hello from pubsub sample", dest="input_message",
                      help="Message payload")
optional.add_argument("--count", type=int, metavar="", default=10, dest="input_count",
                      help="Messages to publish (0 = infinite)")
optional.add_argument("--ca_file", metavar="", dest="input_ca",
                      help="Path to root CA file")
optional.add_argument("--port", type=int, metavar="", default=8883, dest="input_port",
                      help="Connection port")
optional.add_argument("--proxy_host", metavar="", dest="input_proxy_host",
                      help="Proxy hostname")
optional.add_argument("--proxy_port", type=int, metavar="", default=0, dest="input_proxy_port",
                      help="Proxy port")
optional.add_argument("--is_ci", action="store_true", dest="input_is_ci",
                      help="CI mode (suppress some output)")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------

received_count = 0
received_all_event = threading.Event()

# Callback when connection is accidentally lost.


def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    global received_count
    received_count += 1
    if received_count == args.input_count:
        received_all_event.set()

# Callback when the connection successfully connects


def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print("Connection Successful with return code: {} session present: {}".format(
        callback_data.return_code, callback_data.session_present))

# Callback when a connection attempt fails


def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))

# Callback when a connection has been disconnected or shutdown successfully


def on_connection_closed(connection, callback_data):
    print("Connection closed")


if __name__ == '__main__':
    # Create the proxy options if the data is present in args
    proxy_options = None
    if args.input_proxy_host is not None and args.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=args.input_proxy_host,
            port=args.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.input_endpoint,
        port=args.input_port,
        cert_filepath=args.input_cert,
        pri_key_filepath=args.input_key,
        ca_filepath=args.input_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=args.input_clientId,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed)

    if not args.input_is_ci:
        print(f"Connecting to {args.input_endpoint} with client ID '{args.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message_count = args.input_count
    message_topic = args.input_topic
    message_string = args.input_message

    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

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
            message_json = json.dumps(message)
            mqtt_connection.publish(
                topic=message_topic,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(1)
            publish_count += 1

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    if message_count != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")

    received_all_event.wait()
    print("{} message(s) received.".format(received_count))

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
