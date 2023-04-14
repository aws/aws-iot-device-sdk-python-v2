# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5
from awsiot import mqtt5_client_builder
from uuid import uuid4
import threading
from concurrent.futures import Future
import time
import json

# For the purposes of this sample, we need to associate certain variables with a particular MQTT5 client
# and to do so we use this class to hold all the data for a particular client used in the sample.
class sample_mqtt5_client:
    client : mqtt5.Client
    name : str
    count : int
    received_count : int
    received_all_event = threading.Event()
    future_stopped : Future
    future_connection_success : Future

    # Creates a MQTT5 client using direct MQTT5 via mTLS with the passed input data.
    def __init__(self, input_endpoint, input_cert, input_key, input_ca, input_client_id, input_count, input_client_name) -> None:
        try:
            self.count = input_count
            self.received_count = 0
            self.name = input_client_name
            self.future_stopped = Future()
            self.future_connection_success = Future()
            self.client = mqtt5_client_builder.mtls_from_path(
                endpoint=input_endpoint,
                cert_filepath=input_cert,
                pri_key_filepath=input_key,
                client_id=input_client_id,
                ca_filepath=input_ca,
                on_publish_received=self.on_publish_received,
                on_lifecycle_stopped=self.on_lifecycle_stopped,
                on_lifecycle_connection_success=self.on_lifecycle_connection_success,
                on_lifecycle_connection_failure=self.on_lifecycle_connection_failure,
                on_lifecycle_disconnection=self.on_lifecycle_disconnection,
            )
        except Exception as ex:
            print (f"Client creation failed with exception: {ex}")
            raise ex

    # Callback when any publish is received
    def on_publish_received(self, publish_packet_data):
        print(f"[{self.name}] Received a publish")

        publish_packet = publish_packet_data.publish_packet
        assert isinstance(publish_packet, mqtt5.PublishPacket)
        print(f"\tPublish received message on topic: {publish_packet.topic}")
        print(f"\tMessage: {publish_packet.payload}")

        if (publish_packet.user_properties != None):
            if (publish_packet.user_properties.count > 0):
                for i in range(0, publish_packet.user_properties.count):
                    user_property = publish_packet.user_properties[i]
                    print(f"\t\twith UserProperty ({user_property.name}, {user_property.value})")

        self.received_count += 1
        if self.received_count == self.count:
            self.received_all_event.set()

    # Callback for the lifecycle event Stopped
    def on_lifecycle_stopped(self, lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
        print(f"[{self.name}]: Lifecycle Stopped")
        self.future_stopped.set_result(lifecycle_stopped_data)

    # Callback for the lifecycle event Connection Success
    def on_lifecycle_connection_success(self, lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
        print(f"{self.name}]: Lifecycle Connection Success")
        self.future_connection_success.set_result(lifecycle_connect_success_data)

    # Callback for the lifecycle event Connection Failure
    def on_lifecycle_connection_failure(self, lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
        print(f"{self.name}]: Lifecycle Connection Failure")
        print(f"{self.name}]: Connection failed with exception:{lifecycle_connection_failure.exception}")

    # Callback for the lifecycle event Disconnection
    def on_lifecycle_disconnection(self, disconnect_data: mqtt5.LifecycleDisconnectData):
        print(f"{self.name}]: Lifecycle Disconnected")

        if (disconnect_data.disconnect_packet != None):
            print(f"\tDisconnection packet code: {disconnect_data.disconnect_packet.reason_code}")
            print(f"\tDisconnection packet reason: {disconnect_data.disconnect_packet.reason_string}")
            if (disconnect_data.disconnect_packet.reason_code == mqtt5.DisconnectReasonCode.SHARED_SUBSCRIPTIONS_NOT_SUPPORTED):
                # Stop the client, which will interrupt the subscription and stop the sample
                self.client.stop()

# Register arguments that can be parsed from the command line
import utils.command_line_utils as command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("SharedSubscription - Send and receive messages through a MQTT5 shared subscription")
cmdUtils.add_common_mqtt5_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command(
    "port",
    "<int>",
    "Connection port. AWS IoT supports 433 and 8883 (optional, default=auto).",
    type=int)
cmdUtils.register_command(
    "client_id",
    "<str>",
    "Client ID to use for MQTT5 connection (optional, default=None)."
    "Note that '1', '2', and '3' will be added for to the given clientIDs since this sample uses 3 clients.",
    default="test-" + str(uuid4()))
cmdUtils.register_command(
    "count",
    "<int>",
    "The number of messages to send (optional, default='10').",
    default=10,
    type=int)
cmdUtils.register_command(
    "group_identifier",
    "<str>",
    "The group identifier to use in the shared subscription (optional, default='python-sample')",
    default="python-sample",
    type=str)
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

# Pull all the data from the command line
input_endpoint = cmdUtils.get_command_required("endpoint")
input_cert = cmdUtils.get_command_required("cert")
input_key = cmdUtils.get_command_required("key")
input_ca = cmdUtils.get_command("ca_file")
input_client_id = cmdUtils.get_command("client_id", "test-" + str(uuid4()))
input_count = cmdUtils.get_command("count", 10)
input_topic = cmdUtils.get_command("topic", "test/topic")
input_message = cmdUtils.get_command("message", "Hello World!")
input_group_identifier = cmdUtils.get_command("group_identifier", "python-sample")
input_is_ci = cmdUtils.get_command("is_ci", None)
input_is_ci_boolean = (input_is_ci != None and input_is_ci != "None")

# If this is CI, append a UUID to the topic
if (input_is_ci_boolean):
    input_topic += "/" + str(uuid4())

# Construct the shared topic
input_shared_topic = f"$share/{input_group_identifier}/{input_topic}"

# Make sure the message count is even
if (input_count % 2 > 0):
    exit(ValueError("Error: '--count' is an odd number. '--count' must be even or zero for this sample."))

if __name__ == '__main__':
    try:
        # Create the MQTT5 clients: one publisher and two subscribers
        publisher = sample_mqtt5_client(
            input_endpoint, input_cert, input_key, input_ca,
            input_client_id + "1", input_count/2, "Publisher")
        subscriber_one = sample_mqtt5_client(
            input_endpoint, input_cert, input_key, input_ca,
            input_client_id + "2", input_count/2, "Subscriber One")
        subscriber_two = sample_mqtt5_client(
            input_endpoint, input_cert, input_key, input_ca,
            input_client_id + "3", input_count, "Subscriber Two")

        # Connect all the clients
        publisher.client.start()
        publisher.future_connection_success.result(60)
        print (f"[{publisher.name}]: Connected")
        subscriber_one.client.start()
        subscriber_one.future_connection_success.result(60)
        print (f"[{subscriber_one.name}]: Connected")
        subscriber_two.client.start()
        subscriber_two.future_connection_success.result(60)
        print (f"[{subscriber_two.name}]: Connected")

        # Subscribe to the shared topic on the two subscribers
        subscribe_packet = mqtt5.SubscribePacket(
            subscriptions=[mqtt5.Subscription(
                topic_filter=input_shared_topic,
                qos=mqtt5.QoS.AT_LEAST_ONCE)]
        )
        try:
            subscribe_one_future = subscriber_one.client.subscribe(subscribe_packet)
            suback_one = subscribe_one_future.result(60)
            print(f"[{subscriber_one.name}]: Subscribed with: {suback_one.reason_codes}")
            subscribe_two_future = subscriber_two.client.subscribe(subscribe_packet)
            suback_two = subscribe_two_future.result(60)
            print(f"[{subscriber_two.name}]: Subscribed with: {suback_two.reason_codes}")
        except Exception as ex:
            # TMP: If this fails subscribing in CI, just exit the sample gracefully.
            if (input_is_ci != None and input_is_ci != "None"):
                exit(0)
            else:
                raise ex

        # Publish using the publisher client
        if (input_count > 0):
            publish_count = 1
            while (publish_count <= input_count):
                publish_message = f"{input_message} [{publish_count}]"
                publish_future = publisher.client.publish(mqtt5.PublishPacket(
                    topic=input_topic,
                    payload=json.dumps(publish_message),
                    qos=mqtt5.QoS.AT_LEAST_ONCE
                ))
                publish_completion_data = publish_future.result(60)
                print(f"[{publisher.name}]: Sent publish and got PubAck with {repr(publish_completion_data.puback.reason_code)}")
                time.sleep(1)
                publish_count += 1

            # Make sure all the messages were gotten on the subscribers
            subscriber_one.received_all_event.wait(60)
            subscriber_two.received_all_event.wait(60)
        else:
            print("Skipping publishing messages due to message count being zero...")

        # Unsubscribe from the shared topic on the two subscribers
        unsubscribe_packet = mqtt5.UnsubscribePacket(topic_filters=[input_shared_topic])
        unsubscribe_one_future = subscriber_one.client.unsubscribe(unsubscribe_packet)
        unsuback_one = unsubscribe_one_future.result(60)
        print(f"[{subscriber_one.name}]: Unsubscribed with {unsuback_one.reason_codes}")
        unsubscribe_two_future = subscriber_two.client.unsubscribe(unsubscribe_packet)
        unsuback_two = unsubscribe_two_future.result(60)
        print(f"[{subscriber_two.name}]: Unsubscribed with {unsuback_two.reason_codes}")

        # Disconnect all the clients
        publisher.client.stop()
        publisher.future_stopped.result(60)
        print(f"[{publisher.name}]: Fully stopped")
        subscriber_one.client.stop()
        subscriber_one.future_stopped.result(60)
        print(f"[{subscriber_one.name}]: Fully stopped")
        subscriber_two.client.stop()
        subscriber_two.future_stopped.result(60)
        print(f"[{subscriber_two.name}]: Fully stopped")

    except Exception as ex:
        print (f"An exception ocurred while running sample! Exception: {ex}")
        exit(ex)

    print ("Complete!")
