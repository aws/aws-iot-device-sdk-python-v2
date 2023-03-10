# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt
from uuid import uuid4
from concurrent.futures import Future
import os

import mqtt_operation_queue
import utils.command_line_utils as command_line_utils

TEST_TOPIC = "test/topic/" + str(uuid4())
PRINT_QUEUE_LOGS = False


class tester:
    connection: mqtt.Connection
    on_queue_empty_future: Future = Future()
    on_queue_sent_future: Future = Future()
    on_queue_dropped_future: Future = Future()
    cmdUtils: command_line_utils.CommandLineUtils

    def on_application_failure(self, test_name: str, error: Exception):
        print(f"Error in test {test_name}: {error}")
        os._exit(-1)

    def test_connection_setup(self):
        self.connection = self.cmdUtils.build_mqtt_connection(None, None)
        self.on_queue_empty_future: Future = Future()
        self.on_queue_sent_future: Future = Future()
        self.on_queue_dropped_future: Future = Future()

    def test_operation_success(self, result: mqtt_operation_queue.QueueResult, test_name: str):
        if (result != mqtt_operation_queue.QueueResult.SUCCESS):
            self.on_application_failure(test_name, ValueError(
                f"operation was not successful. Result: {result}", test_name))

    def test_connect_sub_pub_unsub(self):
        self.test_connection_setup()
        try:
            def on_queue_empty_future():
                self.on_queue_empty_future.set_result(None)

            def on_queue_sent_future(operation: mqtt_operation_queue.QueueOperation, _):
                self.on_queue_sent_future.set_result(operation)

            def on_queue_dropped_future(operation: mqtt_operation_queue.QueueOperation):
                self.on_queue_dropped_future.set_result(operation)

            queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
            queue_builder.with_connection(self.connection).with_enable_logging(PRINT_QUEUE_LOGS)
            queue_builder.with_on_queue_empty_callback(on_queue_empty_future)
            queue_builder.with_on_operation_sent_callback(on_queue_sent_future)
            queue_builder.with_on_operation_dropped_callback(on_queue_dropped_future)
            mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()

            # Add the operations to the queue
            self.test_operation_success(
                mqtt_queue.subscribe(
                    TEST_TOPIC,
                    mqtt.QoS.AT_LEAST_ONCE,
                    None),
                "test_connect_sub_pub_unsub")
            self.test_operation_success(
                mqtt_queue.publish(
                    TEST_TOPIC,
                    "hello_world",
                    mqtt.QoS.AT_LEAST_ONCE),
                "test_connect_sub_pub_unsub")
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_connect_sub_pub_unsub")

            if (mqtt_queue.get_queue_size() != 3):
                self.on_application_failure("test_connect_sub_pub_unsub", ValueError("Queue size is not 3"))

            connect_future = self.connection.connect()
            connect_future.result()
            mqtt_queue.start()

            # Make sure the order is right. Order should be: Sub, Pub, Unsub
            return_operation: mqtt_operation_queue.QueueOperation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type != mqtt_operation_queue.QueueOperationType.SUBSCRIBE):
                self.on_application_failure("test_connect_sub_pub_unsub", ValueError(
                    f"First operation is not subscribe. Type is {return_operation.type}"))
            self.on_queue_sent_future = Future()  # reset future
            return_operation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type != mqtt_operation_queue.QueueOperationType.PUBLISH):
                self.on_application_failure("test_connect_sub_pub_unsub", ValueError(
                    f"Second operation is not publish. Type is {return_operation.type}"))
            self.on_queue_sent_future = Future()  # reset future
            return_operation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type !=
                    mqtt_operation_queue.QueueOperationType.UNSUBSCRIBE):
                self.on_application_failure("test_connect_sub_pub_unsub", ValueError(
                    f"Third operation is not unsubscribe. Type is {return_operation.type}"))

            self.on_queue_empty_future.result()
            mqtt_queue.stop()
            disconnect_future = self.connection.disconnect()
            disconnect_future.result()
        except Exception as ex:
            self.on_application_failure("test_connect_sub_pub_unsub", ex)

    def test_drop_back(self):
        self.test_connection_setup()
        try:
            def on_queue_empty_future():
                self.on_queue_empty_future.set_result(None)

            def on_queue_sent_future(operation: mqtt_operation_queue.QueueOperation, _):
                self.on_queue_sent_future.set_result(operation)

            def on_queue_dropped_future(operation: mqtt_operation_queue.QueueOperation):
                self.on_queue_dropped_future.set_result(operation)

            queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
            queue_builder.with_connection(self.connection).with_enable_logging(PRINT_QUEUE_LOGS)
            queue_builder.with_on_queue_empty_callback(on_queue_empty_future)
            queue_builder.with_on_operation_sent_callback(on_queue_sent_future)
            queue_builder.with_on_operation_dropped_callback(on_queue_dropped_future)
            queue_builder.with_queue_limit_size(2).with_queue_limit_behavior(
                mqtt_operation_queue.LimitBehavior.DROP_BACK)
            mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()

            # Add the operations to the queue
            self.test_operation_success(
                mqtt_queue.subscribe(
                    TEST_TOPIC,
                    mqtt.QoS.AT_LEAST_ONCE,
                    None),
                "test_drop_back")

            # Add 10 publishes
            for i in range(0, 10):
                self.on_queue_dropped_future = Future()  # reset future
                self.test_operation_success(
                    mqtt_queue.publish(
                        TEST_TOPIC,
                        "hello_world",
                        mqtt.QoS.AT_LEAST_ONCE),
                    "test_drop_back")

            if (mqtt_queue.get_queue_size() != 2):
                self.on_application_failure("test_drop_back", ValueError("Queue size is not 2"))

            self.on_queue_dropped_future = Future()  # reset future
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_drop_back")
            dropped_operation: mqtt_operation_queue.QueueOperation = self.on_queue_dropped_future.result()
            if (dropped_operation is None or dropped_operation.type != mqtt_operation_queue.QueueOperationType.PUBLISH):
                self.on_application_failure("test_drop_back", ValueError(
                    f"Dropped operation is not publish. Type is {dropped_operation.type}"))

            connect_future = self.connection.connect()
            connect_future.result()
            mqtt_queue.start()

            # Make sure the order is right. Order should be: Sub, Unsub
            return_operation: mqtt_operation_queue.QueueOperation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type != mqtt_operation_queue.QueueOperationType.SUBSCRIBE):
                self.on_application_failure("test_drop_back", ValueError(
                    f"First operation is not subscribe. Type is {return_operation.type}"))
            self.on_queue_sent_future = Future()  # reset future
            return_operation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type !=
                    mqtt_operation_queue.QueueOperationType.UNSUBSCRIBE):
                self.on_application_failure("test_drop_back", ValueError(
                    f"Second operation is not unsubscribe. Type is {return_operation.type}"))

            self.on_queue_empty_future.result()
            mqtt_queue.stop()
            disconnect_future = self.connection.disconnect()
            disconnect_future.result()
        except Exception as ex:
            self.on_application_failure("test_drop_back", ex)

    def test_drop_front(self):
        self.test_connection_setup()
        try:
            def on_queue_dropped_future(operation: mqtt_operation_queue.QueueOperation):
                self.on_queue_dropped_future.set_result(operation)

            queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
            queue_builder.with_connection(self.connection).with_enable_logging(PRINT_QUEUE_LOGS)
            queue_builder.with_on_operation_dropped_callback(on_queue_dropped_future)
            queue_builder.with_queue_limit_size(2).with_queue_limit_behavior(
                mqtt_operation_queue.LimitBehavior.DROP_FRONT)
            mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()

            # Add the operations to the queue
            self.test_operation_success(
                mqtt_queue.subscribe(
                    TEST_TOPIC,
                    mqtt.QoS.AT_LEAST_ONCE,
                    None),
                "test_drop_front")
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_drop_front")

            if (mqtt_queue.get_queue_size() != 2):
                self.on_application_failure("test_drop_front", ValueError("Queue size is not 2"))

            # Add two publishes, make sure drop order is correct
            self.test_operation_success(
                mqtt_queue.publish(
                    TEST_TOPIC,
                    "hello_world",
                    mqtt.QoS.AT_LEAST_ONCE),
                "test_drop_front")
            dropped_operation: mqtt_operation_queue.QueueOperation = self.on_queue_dropped_future.result()
            if (dropped_operation is None or dropped_operation.type !=
                    mqtt_operation_queue.QueueOperationType.SUBSCRIBE):
                self.on_application_failure("test_drop_front", ValueError(
                    f"First Dropped operation is not subscribe. Type is {dropped_operation.type}"))
            # second drop
            self.on_queue_dropped_future = Future()  # reset future
            self.test_operation_success(
                mqtt_queue.publish(
                    TEST_TOPIC,
                    "hello_world",
                    mqtt.QoS.AT_LEAST_ONCE),
                "test_drop_front")
            dropped_operation = self.on_queue_dropped_future.result()
            if (dropped_operation is None or dropped_operation.type !=
                    mqtt_operation_queue.QueueOperationType.UNSUBSCRIBE):
                self.on_application_failure("test_drop_front", ValueError(
                    f"First Dropped operation is not unsubscribe. Type is {dropped_operation.type}"))

        except Exception as ex:
            self.on_application_failure("test_drop_front", ex)

    def test_add_front(self):
        self.test_connection_setup()
        try:
            def on_queue_empty_future():
                self.on_queue_empty_future.set_result(None)

            def on_queue_sent_future(operation: mqtt_operation_queue.QueueOperation, _):
                self.on_queue_sent_future.set_result(operation)

            queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
            queue_builder.with_connection(self.connection).with_enable_logging(PRINT_QUEUE_LOGS)
            queue_builder.with_on_queue_empty_callback(on_queue_empty_future)
            queue_builder.with_on_operation_sent_callback(on_queue_sent_future)
            queue_builder.with_queue_limit_size(2).with_queue_limit_behavior(
                mqtt_operation_queue.LimitBehavior.DROP_BACK)
            queue_builder.with_queue_insert_behavior(mqtt_operation_queue.InsertBehavior.INSERT_FRONT)
            mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()

            # Fill with publishes
            self.test_operation_success(
                mqtt_queue.publish(
                    TEST_TOPIC,
                    "hello_world",
                    mqtt.QoS.AT_LEAST_ONCE),
                "test_add_front")
            self.test_operation_success(
                mqtt_queue.publish(
                    TEST_TOPIC,
                    "hello_world",
                    mqtt.QoS.AT_LEAST_ONCE),
                "test_add_front")

            if (mqtt_queue.get_queue_size() != 2):
                self.on_application_failure("test_add_front", ValueError("Queue size is not 2"))

            # Add unsubscribe than subscribe, which should result in the queue order of subscribe, unsubscribe
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_add_front")
            self.test_operation_success(
                mqtt_queue.subscribe(
                    TEST_TOPIC,
                    mqtt.QoS.AT_LEAST_ONCE,
                    None),
                "test_add_front")

            if (mqtt_queue.get_queue_size() != 2):
                self.on_application_failure("test_add_front", ValueError("Queue size is not 2"))

            connect_future = self.connection.connect()
            connect_future.result()
            mqtt_queue.start()

            # Make sure the order is right. Order should be: Sub, Unsub
            return_operation: mqtt_operation_queue.QueueOperation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type != mqtt_operation_queue.QueueOperationType.SUBSCRIBE):
                self.on_application_failure("test_add_front", ValueError(
                    f"First operation is not subscribe. Type is {return_operation.type}"))
            self.on_queue_sent_future = Future()  # reset future
            return_operation = self.on_queue_sent_future.result()
            if (return_operation is None or return_operation.type !=
                    mqtt_operation_queue.QueueOperationType.UNSUBSCRIBE):
                self.on_application_failure("test_add_front", ValueError(
                    f"Second operation is not unsubscribe. Type is {return_operation.type}"))

            self.on_queue_empty_future.result()
            mqtt_queue.stop()

            disconnect_future = self.connection.disconnect()
            disconnect_future.result()

        except Exception as ex:
            self.on_application_failure("test_add_front", ex)

    def test_add_error(self):
        self.test_connection_setup()
        try:
            queue_builder = mqtt_operation_queue.MqttOperationQueueBuilder()
            queue_builder.with_connection(self.connection).with_enable_logging(PRINT_QUEUE_LOGS)
            queue_builder.with_queue_limit_size(2).with_queue_limit_behavior(
                mqtt_operation_queue.LimitBehavior.RETURN_ERROR)
            mqtt_queue: mqtt_operation_queue.MqttOperationQueue = queue_builder.build()
            # Fill with unsubscribe
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_add_error")
            self.test_operation_success(mqtt_queue.unsubscribe(TEST_TOPIC), "test_add_error")
            # Try to add another but it should return error stating queue is full
            operation_result: mqtt_operation_queue.QueueResult = mqtt_queue.unsubscribe(TEST_TOPIC)
            if (operation_result != mqtt_operation_queue.QueueResult.ERROR_QUEUE_FULL):
                self.on_application_failure("test_add_error", ValueError(
                    "Did not return queue full error trying to add operation to full queue"))

        except Exception as ex:
            self.on_application_failure("test_add_error", ex)

    def perform_tests(self):
        print("Starting test_connect_sub_pub_unsub test")
        self.test_connect_sub_pub_unsub()
        print("Finished test_connect_sub_pub_unsub test")

        print("Starting test_drop_back test")
        self.test_drop_back()
        print("Finished test_drop_back test")

        print("Starting test_drop_front test")
        self.test_drop_front()
        print("Finished test_drop_front test")

        print("Starting test_add_front test")
        self.test_add_front()
        print("Finished test_add_front test")

        print("Starting test_add_error test")
        self.test_add_error()
        print("Finished test_add_error test")


def perform_tests(cmdUtils: command_line_utils.CommandLineUtils):
    tests = tester()
    tests.cmdUtils = cmdUtils
    tests.perform_tests()
    print("All tests finished. Exiting...")
    os._exit(0)
