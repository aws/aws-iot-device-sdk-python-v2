# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
import argparse
from awscrt import io, mqtt
import threading
import time

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--cert', required=True, help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', required=True, help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")
parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
parser.add_argument('--topic', default="samples/test", help="Topic to subscribe to, and publish messages to.")
parser.add_argument('--message', default="Hello World!", help="Message to publish. " +
                                                              "Specify empty string to publish nothing.")
parser.add_argument('--count', default=10, type=int, help="Number of messages to publish/receive before exiting. " +
                                                          "Specify 0 to run forever.")
# Using globals to simplify sample code
args = parser.parse_args()

received_count = 0
received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(error_code):
    print("Connection interrupted. error_code:{}".format(error_code))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(error_code, session_present):
    print("Connection resumed. error_code:{} session_present:{}".format(error_code, session_present))

# Callback when the subscribed topic receives a message
def on_message_received(topic, message):
    print("Received message from topic '{}': {}".format(topic, message))
    global received_count
    received_count += 1
    if received_count == args.count:
        received_all_event.set()

if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    client_bootstrap = io.ClientBootstrap(event_loop_group)

    tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.cert, args.key)
    if args.root_ca:
        tls_options.override_default_trust_store_from_path(ca_path=None, ca_file=args.root_ca)
    tls_context = io.ClientTlsContext(tls_options)

    mqtt_client = mqtt.Client(client_bootstrap, tls_context)

    # Create connection
    port = 8883

    print("Connecting to {} on port {} with client ID '{}'...".format(
        args.endpoint, port, args.client_id))

    mqtt_connection = mqtt.Connection(
        client=mqtt_client,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed)

    connect_future = mqtt_connection.connect(
        client_id=args.client_id,
        host_name = args.endpoint,
        port = port,
        use_websocket=False,
        clean_session=True,
        keep_alive=6000)

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Subscribe
    print("Subscribing to topic '{}'...".format(args.topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=args.topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_future.result()
    print("Subscribed!")

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    if args.message:
        if args.count == 0:
            print ("Sending messages until program killed")
        else:
            print ("Sending {} message(s)".format(args.count))

        publish_count = 1
        while (publish_count <= args.count) or (args.count == 0):
            message = "{} [{}]".format(args.message, publish_count)
            print("Publishing message to topic '{}': {}".format(args.topic, message))
            mqtt_connection.publish(
                topic=args.topic,
                payload=message,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(1)
            publish_count += 1

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    if args.count != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")

    received_all_event.wait()
    print("{} message(s) received.".format(received_count))

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
