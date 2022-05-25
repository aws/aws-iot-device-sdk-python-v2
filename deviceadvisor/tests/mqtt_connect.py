# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt_connection_builder
from da_test_utils import DATestUtils, TestType

# This sample used to test mqtt connection through device advisor

if __name__ == '__main__':
    # init variables
    utils = DATestUtils.valid(TestType.CONNECT)
    if not utils:
        quit(-1)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=DATestUtils.endpoint,
        cert_filepath=DATestUtils.certificatePath,
        pri_key_filepath=DATestUtils.keyPath,
        client_id = DATestUtils.client_id,
        clean_session = True, 
        ping_timeout_ms = 6000)

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    quit(0)
