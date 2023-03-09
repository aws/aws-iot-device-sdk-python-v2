# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt
import threading
from uuid import uuid4
import json
from concurrent.futures import Future

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection, but uses a MQTT operation queue instead of
# directly using the MQTT connection to perform operations.

import mqtt_operation_queue
import mqtt_operation_queue_tests

# Parse arguments
from command_line_utils import CommandLineUtils
cmdUtils = CommandLineUtils("Operation Queue Sample")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command("port", "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
cmdUtils.register_command("client_id", "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
cmdUtils.register_command("count", "<int>", "The number of messages to send (optional, default='20').", default=20, type=int)
cmdUtils.register_command("queue_limit", "<int>", "The maximum number of operations for the queue (optional, default='10')", default=10, type=int)
cmdUtils.register_command("queue_mode", "<int>", "The mode for the queue to use (optional, default=0)" +
                          "\n\t0 = Overflow removes from queue back and new operations are pushed to queue back" +
                          "\n\t1 = Overflow removes from queue front and new operations are pushed to queue back" +
                          "\n\t2 = Overflow removes from queue front and new operations are pushed to queue front" +
                          "\n\t3 = Overflow removes from queue back and new operations are pushed to queue front",
                          default=10, type=int)
cmdUtils.register_command("run_tests", "<int>",
                          "If set to True (1 or greater), then the queue tests will be run instead of the sample (optional, default=0)",
                          default=0, type=int)
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")

# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

received_count = 0
received_all_event = threading.Event()
is_ci = cmdUtils.get_command("is_ci", None) is not None

if (cmdUtils.get_command("run_tests") > 0):
    mqtt_operation_queue_tests.perform_tests(cmdUtils)

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        connection.resubscribe_existing_topics()

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    global received_count
    received_count += 1
    if received_count == cmdUtils.get_command("queue_limit"):
        received_all_event.set()


# Callback when the mqtt operation queue is completely empty
queue_empty_future = Future()
def on_queue_empty():
    print("Queue is completely empty!")
    global queue_empty_future
    queue_empty_future.set_result(None)

# Callback when the mqtt operation queue is full
def on_queue_full():
    print("Operation queue is full and will start dropping operations should new operations come in")

# Callback when the mqtt operation queue sends an operation
def on_queue_operation_sent(operation: mqtt_operation_queue.QueueOperation, _):
    if (operation.type == mqtt_operation_queue.QueueOperationType.PUBLISH):
        print(f"Sending publish with payload [{operation.payload}] from the operation queue")
    else:
        print(f"Sending operation of type {operation.type} from the operation queue")

# Callback when the mqtt operation queue fails to send an operation
def on_queue_operation_sent_failure(
        operation: mqtt_operation_queue.QueueOperation,
        error: mqtt_operation_queue.QueueResult):
    print(f"ERROR: Operation from queue with type {operation.type} failed with error {error}")

# Callback when the mqtt operation queue drops an operation from the queue
def on_queue_operation_dropped(operation: mqtt_operation_queue.QueueOperation):
    if (operation.type == mqtt_operation_queue.QueueOperationType.PUBLISH):
        print(f"Publish with payload [{operation.payload}] dropped from the operation queue")
    else:
        print(f"Operation of type {operation.type} dropped from the operation queue")


if __name__ == '__main__':
    mqtt_connection = cmdUtils.build_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
    queue_builder.with_connection(mqtt_connection).with_queue_limit_size(cmdUtils.get_command("queue_limit"))
    queue_builder.with_on_queue_empty_callback(on_queue_empty)
    queue_builder.with_on_queue_full_callback(on_queue_full)
    queue_builder.with_on_operation_sent_callback(on_queue_operation_sent)
    queue_builder.with_on_operation_sent_failure_callback(on_queue_operation_sent_failure)
    queue_builder.with_on_operation_dropped_callback(on_queue_operation_dropped)
    if (cmdUtils.get_command("queue_mode") == 0):
        queue_builder.with_queue_insert_behavior(mqtt_operation_queue.InsertBehavior.INSERT_BACK)
        queue_builder.with_queue_limit_behavior(mqtt_operation_queue.LimitBehavior.DROP_BACK)
    elif (cmdUtils.get_command("queue_mode") == 1):
        queue_builder.with_queue_insert_behavior(mqtt_operation_queue.InsertBehavior.INSERT_BACK)
        queue_builder.with_queue_limit_behavior(mqtt_operation_queue.LimitBehavior.DROP_FRONT)
    elif (cmdUtils.get_command("queue_mode") == 2):
        queue_builder.with_queue_insert_behavior(mqtt_operation_queue.InsertBehavior.INSERT_FRONT)
        queue_builder.with_queue_limit_behavior(mqtt_operation_queue.LimitBehavior.DROP_FRONT)
    elif (cmdUtils.get_command("queue_mode") == 3):
        queue_builder.with_queue_insert_behavior(mqtt_operation_queue.InsertBehavior.INSERT_FRONT)
        queue_builder.with_queue_limit_behavior(mqtt_operation_queue.LimitBehavior.DROP_BACK)
    mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()

    if not is_ci:
        print("Connecting to {} with client ID '{}'...".format(
            cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Start the queue
    mqtt_queue.start()

    message_count = cmdUtils.get_command("count")
    message_topic = cmdUtils.get_command(cmdUtils.m_cmd_topic)
    message_string = cmdUtils.get_command(cmdUtils.m_cmd_message)

    # Subscribe using the queue
    print("Subscribing to topic '{}'...".format(message_topic))
    mqtt_queue.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    # Wait for the queue to be empty, indicating the subscribe was sent
    queue_empty_future.result()

    # Reset the queue empty future
    queue_empty_future = Future()
    # Publish message to server desired number of times using the operation queue.
    # This step is skipped if message is blank.
    if message_string and message_count > 0:
        print(f"Filling queue with {message_count} message(s)")

        publish_count = 1
        while (publish_count <= message_count) or (message_count == 0):
            message = "{} [{}]".format(message_string, publish_count)
            # print(f"Publishing message to topic '{message_topic}': {message}")
            message_json = json.dumps(message)
            mqtt_queue.publish(
                topic=message_topic,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            publish_count += 1

        # wait for the queue to be empty
        print("Waiting for all publishes in queue to be sent...")
        queue_empty_future.result()
    else:
        print("Skipping sending publishes due to message being blank or message count being zero")

    # Wait for all messages to be received and ACKs to be back from the server
    if message_count != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")
        received_all_event.wait()
        print("{} message(s) received.".format(received_count))

    # Reset the queue empty future
    queue_empty_future = Future()
    # Unsubscribe using the operation queue
    mqtt_queue.unsubscribe(message_topic)
    # Wait for the queue to be empty, indicating the unsubscribe was sent
    queue_empty_future.result()

    # Stop the queue
    mqtt_queue.stop()

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
