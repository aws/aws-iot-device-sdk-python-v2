# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import json

# This sample is similar to `samples/pubsub.py` but the private key
# for mutual TLS is stored on a PKCS#11 compatible smart card or
# Hardware Security Module (HSM).
#
# See `samples/README.md` for instructions on setting up your PKCS#11 device
# to run this sample.
#
# WARNING: Unix only. Currently, TLS integration with PKCS#11 is only available on Unix devices.

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--port', type=int, help="Specify port. AWS IoT supports 443 and 8883. (default: auto)")
parser.add_argument('--cert', required=True, help="File path to your client certificate, in PEM format.")
parser.add_argument('--pkcs11-lib', required=True, help="Path to PKCS#11 library.")
parser.add_argument('--pin', required=True, help="User PIN for logging into PKCS#11 token.")
parser.add_argument('--token-label', help="Label of PKCS#11 token to use. (default: None) ")
parser.add_argument('--slot-id', help="Slot ID containing PKCS#11 token to use. (default: None)")
parser.add_argument('--key-label', help="Label of private key on the PKCS#11 token. (default: None)")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. (default: None)")
parser.add_argument('--client-id', default="test-" + str(uuid4()),
                    help="Client ID for MQTT connection. (default: 'test-*')")
parser.add_argument('--topic', default="test/topic",
                    help="Topic to subscribe to, and publish messages to. (default: 'test/topic')")
parser.add_argument('--message', default="Hello World!",
                    help="Message to publish. Specify empty string to publish nothing. (default: 'Hello World!')")
parser.add_argument('--count', default=10, type=int, help="Number of messages to publish/receive before exiting. " +
                                                          "Specify 0 to run forever. (default: 10)")
parser.add_argument('--verbosity', choices=[x.name for x in io.LogLevel], default=io.LogLevel.NoLogs.name,
                    help="Logging level. (default: 'NoLogs')")

# Using globals to simplify sample code
args = parser.parse_args()

io.init_logging(getattr(io.LogLevel, args.verbosity), 'stderr')

received_count = 0
received_all_event = threading.Event()


def on_connection_interrupted(connection, error, **kwargs):
    # Callback when connection is accidentally lost.
    print("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    # Callback when an interrupted connection is re-established.
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    global received_count
    received_count += 1
    if received_count == args.count:
        received_all_event.set()


if __name__ == '__main__':
    print(f"Loading PKCS#11 library '{args.pkcs11_lib}' ...")
    pkcs11_lib = io.Pkcs11Lib(
        file=args.pkcs11_lib,
        behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
    print("Loaded!")

    # Create MQTT connection
    mqtt_connection = mqtt_connection_builder.mtls_with_pkcs11(
        pkcs11_lib=pkcs11_lib,
        user_pin=args.pin,
        slot_id=int(args.slot_id) if args.slot_id else None,
        token_label=args.token_label,
        private_key_label=args.key_label,
        cert_filepath=args.cert,
        endpoint=args.endpoint,
        port=args.port,
        ca_filepath=args.root_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=30)

    print("Connecting to {} with client ID '{}'...".format(
        args.endpoint, args.client_id))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Subscribe
    print("Subscribing to topic '{}'...".format(args.topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=args.topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    if args.message:
        if args.count == 0:
            print("Sending messages until program killed")
        else:
            print("Sending {} message(s)".format(args.count))

        publish_count = 1
        while (publish_count <= args.count) or (args.count == 0):
            message = "{} [{}]".format(args.message, publish_count)
            print("Publishing message to topic '{}': {}".format(args.topic, message))
            message_json = json.dumps(message)
            mqtt_connection.publish(
                topic=args.topic,
                payload=message_json,
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
