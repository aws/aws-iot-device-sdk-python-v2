# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5
from awsiot import mqtt5_client_builder
import threading
from concurrent.futures import Future
import time
import json
from utils.command_line_utils import CommandLineUtils

# For the purposes of this sample, we need to associate certain variables with a particular MQTT5 client
# and to do so we use this class to hold all the data for a particular client used in the sample.
class sample_mqtt5_client:
    client: mqtt5.Client
    name: str
    count: int
    future_stopped: Future
    future_connection_success: Future

    # Creates a MQTT5 client using direct MQTT5 via mTLS with the passed input data.
    def __init__(
            self,
            input_endpoint,
            input_cert,
            input_key,
            input_ca,
            input_client_id,
            input_client_name) -> None:
        try:
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
            print(f"Client creation failed with exception: {ex}")
            raise ex

    # Callback when any publish is received
    def on_publish_received(self, publish_packet_data):
        print(f"[{self.name}] Received a publish")

        publish_packet = publish_packet_data.publish_packet
        assert isinstance(publish_packet, mqtt5.PublishPacket)
        print(f"\tPublish received message on topic: {publish_packet.topic}")
        print(f"\tMessage: {publish_packet.payload}")

        if (publish_packet.user_properties is not None):
            if (publish_packet.user_properties.count > 0):
                for i in range(0, publish_packet.user_properties.count):
                    user_property = publish_packet.user_properties[i]
                    print(f"\t\twith UserProperty ({user_property.name}, {user_property.value})")

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

        if (disconnect_data.disconnect_packet is not None):
            print(f"\tDisconnection packet code: {disconnect_data.disconnect_packet.reason_code}")
            print(f"\tDisconnection packet reason: {disconnect_data.disconnect_packet.reason_string}")
            if (disconnect_data.disconnect_packet.reason_code ==
                    mqtt5.DisconnectReasonCode.SHARED_SUBSCRIPTIONS_NOT_SUPPORTED):
                # Stop the client, which will interrupt the subscription and stop the sample
                self.client.stop()


# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_mqtt5_shared_subscription()

# Construct the shared topic
input_shared_topic = f"$share/{cmdData.input_group_identifier}/{cmdData.input_topic}"

if __name__ == '__main__':
    try:
        # Create the MQTT5 clients: one publisher and two subscribers
        publisher = sample_mqtt5_client(
            cmdData.input_endpoint, cmdData.input_cert, cmdData.input_key, cmdData.input_ca,
            cmdData.input_clientId + "1", "Publisher")
        subscriber_one = sample_mqtt5_client(
            cmdData.input_endpoint, cmdData.input_cert, cmdData.input_key, cmdData.input_ca,
            cmdData.input_clientId + "2", "Subscriber One")
        subscriber_two = sample_mqtt5_client(
            cmdData.input_endpoint, cmdData.input_cert, cmdData.input_key, cmdData.input_ca,
            cmdData.input_clientId + "3", "Subscriber Two")

        # Connect all the clients
        publisher.client.start()
        publisher.future_connection_success.result(60)
        print(f"[{publisher.name}]: Connected")
        subscriber_one.client.start()
        subscriber_one.future_connection_success.result(60)
        print(f"[{subscriber_one.name}]: Connected")
        subscriber_two.client.start()
        subscriber_two.future_connection_success.result(60)
        print(f"[{subscriber_two.name}]: Connected")

        # Subscribe to the shared topic on both subscribers
        subscribe_packet = mqtt5.SubscribePacket(
            subscriptions=[mqtt5.Subscription(
                topic_filter=input_shared_topic,
                qos=mqtt5.QoS.AT_LEAST_ONCE)]
        )
        subscribe_one_future = subscriber_one.client.subscribe(subscribe_packet)
        suback_one = subscribe_one_future.result(60)
        print(f"[{subscriber_one.name}]: Subscribed to topic '{cmdData.input_topic}' in shared subscription group '{cmdData.input_group_identifier}'.")
        print(f"[{subscriber_one.name}]: Full subscribed topic is: '{input_shared_topic}' with SubAck code: {suback_one.reason_codes}")
        subscribe_two_future = subscriber_two.client.subscribe(subscribe_packet)
        suback_two = subscribe_two_future.result(60)
        print(f"[{subscriber_two.name}]: Subscribed to topic '{cmdData.input_topic}' in shared subscription group '{cmdData.input_group_identifier}'.")
        print(f"[{subscriber_two.name}]: Full subscribed topic is: '{input_shared_topic}' with SubAck code: {suback_two.reason_codes}")

        # Publish using the publisher client
        if (cmdData.input_count > 0):
            publish_count = 1
            while (publish_count <= cmdData.input_count):
                publish_message = f"{cmdData.input_message} [{publish_count}]"
                publish_future = publisher.client.publish(mqtt5.PublishPacket(
                    topic=cmdData.input_topic,
                    payload=json.dumps(publish_message),
                    qos=mqtt5.QoS.AT_LEAST_ONCE
                ))
                publish_completion_data = publish_future.result(60)
                print(f"[{publisher.name}]: Sent publish and got PubAck code: {repr(publish_completion_data.puback.reason_code)}")
                time.sleep(1)
                publish_count += 1

            # Wait 5 seconds to let the last publish go out before unsubscribing
            time.sleep(5)
        else:
            print("Skipping publishing messages due to message count being zero...")

        # Unsubscribe from the shared topic on the two subscribers
        unsubscribe_packet = mqtt5.UnsubscribePacket(topic_filters=[input_shared_topic])
        unsubscribe_one_future = subscriber_one.client.unsubscribe(unsubscribe_packet)
        unsuback_one = unsubscribe_one_future.result(60)
        print(f"[{subscriber_one.name}]: Unsubscribed to topic '{cmdData.input_topic}' in shared subscription group '{cmdData.input_group_identifier}'.")
        print(f"[{subscriber_one.name}]: Full unsubscribed topic is: '{input_shared_topic}' with UnsubAck code: {unsuback_one.reason_codes}")
        unsubscribe_two_future = subscriber_two.client.unsubscribe(unsubscribe_packet)
        unsuback_two = unsubscribe_two_future.result(60)
        print(f"[{subscriber_two.name}]: Unsubscribed to topic '{cmdData.input_topic}' in shared subscription group '{cmdData.input_group_identifier}'.")
        print(f"[{subscriber_two.name}]: Full unsubscribed topic is: '{input_shared_topic}' with UnsubAck code {unsuback_two.reason_codes}")

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
        print(f"An exception ocurred while running sample! Exception: {ex}")
        exit(ex)

    print("Complete!")
