# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt
from awsiot import iotshadow, mqtt_connection_builder
from concurrent.futures import Future
from da_test_utils import DATestUtils, TestType
from uuid import uuid4

if __name__ == '__main__':
    # init variables
    utils = DATestUtils.valid(TestType.SUB_PUB)
    if not utils:
        quit(-1)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint = DATestUtils.endpoint,
        cert_filepath = DATestUtils.certificatePath,
        pri_key_filepath = DATestUtils.keyPath,
        client_id = DATestUtils.generate_client_id("-shadow"),
        clean_session = True,
        tcp_connect_timeout_ms = 60000, # 1 minute
        keep_alive_secs = 60000, # 1 minute
        ping_timeout_ms = 120000) # 2 minutes

    connect_future = mqtt_connection.connect()
    connect_future.result()
    shadow_client = iotshadow.IotShadowClient(mqtt_connection)

    # Publish shadow value
    request = iotshadow.UpdateShadowRequest(
        thing_name=DATestUtils.thing_name,
        state=iotshadow.ShadowState(
            reported={ DATestUtils.shadowProperty: DATestUtils.shadowValue },
            desired={ DATestUtils.shadowProperty: DATestUtils.shadowValue },
        )
    )
    # Device advisor test will not return PUBACK, therefore we use AT_MOST_ONCE so that
    # we dont busy wait for PUBACK
    shadow_future = shadow_client.publish_update_shadow(request, mqtt.QoS.AT_MOST_ONCE)
    shadow_future.result()

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    quit(0)
