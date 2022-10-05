# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from da_test_utils import DATestUtils, TestType
import json

if __name__ == '__main__':
    # validate environment variables
    utils = DATestUtils.valid(TestType.SUB_PUB)
    if not utils:
        quit(-1)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint = DATestUtils.endpoint,
        cert_filepath = DATestUtils.certificatePath,
        pri_key_filepath = DATestUtils.keyPath,
        client_id = DATestUtils.generate_client_id("-pub"),
        clean_session = True,
        tcp_connect_timeout_ms = 60000, # 1 minute
        keep_alive_secs = 60000, # 1 minute
        ping_timeout_ms = 120000) # 2 minutes
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()

    message = "Hello World"
    message_json = json.dumps(message)
    # Device advisor test will not return PUBACK, therefore we use AT_MOST_ONCE so that
    # we dont busy wait for PUBACK
    publish_future, packet_id = mqtt_connection.publish(
        topic=DATestUtils.topic,
        payload=message_json,
        qos=mqtt.QoS.AT_MOST_ONCE)
    publish_future.result()

    # Disconnect
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    quit(0)
