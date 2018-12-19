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
from aws_crt import io, mqtt
import threading
import time

# This sample uses the Message Broken for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broken,
# since it is subscribed to that same topic.

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"w6zbse3vjd5b4p-ats.iot.us-west-2.amazonaws.com\"")
parser.add_argument('--cert', required=True, help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', required=True, help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")
parser.add_argument('--topic', default="sample/test", help="Topic to subscribe to, and publish messages to.")
parser.add_argument('--message', default="Hello World!", help="Message to publish. " +
                                                              "Specify empty string to publish nothing.")
parser.add_argument('--count', default=10, type=int, help="Number of messages to publish/receive before exiting. " +
                                                          "Specify 0 to run forever.")
# Using globals to simplify sample code
args = parser.parse_args()

connected_results = {}
connected_event = threading.Event()

disconnect_called = False
disconnected_results = {}
disconnected_event = threading.Event()

subscribed_event = threading.Event()

received_count = 0
received_all_event = threading.Event()

# Callback when connection is established.
# This may be an initial connection, or a reconnect
# after an accidentally losing the connection.
def on_connected(return_code, session_present):
    if not connected_results:
        connected_results['return_code'] = return_code
        connected_results['session_present'] = session_present
        connected_event.set()
    else:
        print("Connection re-established!")

# Callback when connection is lost.
# This may be due to a purposeful disconnect() call,
# or it may be an accidental loss of the connection.
# Return True to attempt reconnecting.
def on_disconnected(return_code):
    if disconnect_called:
        disconnected_results['return_code'] = return_code
        disconnected_event.set()
        return False
    else:
        print("Connection lost. Attempting to reconnect...")
        return True

# Callback when async subscribe operation completes
def on_subscribed(packet_id, topic, qos):
    subscribed_event.set()

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

    tls_options = io.TlsContextOptions.create_client_with_mtls(args.cert, args.key)
    if args.root_ca:
        tls_options.override_default_trust_store(ca_path=None, ca_file=args.root_ca)
    tls_context = io.ClientTlsContext(tls_options)

    mqtt_client = mqtt.Client(client_bootstrap, tls_context)
    mqtt_connection = mqtt.Connection(mqtt_client, 'samples_client_id')

    # Connect
    port = 443 if io.is_alpn_available() else 8883
    print("Connecting to {} on port {}...".format(args.endpoint, port))
    mqtt_connection.connect(
            host_name = args.endpoint,
            port = port,
            on_connect=on_connected,
            on_disconnect=on_disconnected,
            use_websocket=False,
            alpn=None,
            clean_session=True,
            keep_alive=6000)

    connected_event.wait()
    connected_code = connected_results['return_code']
    if connected_code != 0:
        raise RuntimeError("Connection failed with return code: {}".format(connected_code))
    print('Connected!')

    # Subscribe
    print("Subscribing to topic '{}'...".format(args.topic))
    mqtt_connection.subscribe(topic=args.topic, qos=1,
        suback_callback=on_subscribed, callback=on_message_received)

    subscribed_event.wait()
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
                qos=1)
            time.sleep(1)
            publish_count += 1

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    received_all_event.wait()
    print("{} message(s) received.".format(received_count))

    # Disconnect
    print("Disconnecting...")
    disconnect_called = True
    mqtt_connection.disconnect()
    disconnected_event.wait()
    disconnected_code = disconnected_results['return_code']
    if disconnected_code != 0:
        raise RuntimeError("Disconnected with return code: {}".format(disconnected_code))
    print("Disconnected!")
