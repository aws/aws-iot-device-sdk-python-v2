# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt_connection_builder
from utils.command_line_utils import CommandLineUtils

# This sample is similar to `samples/basic_connect.py` but it connects
# through a custom authorizer rather than using a key and certificate.

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_custom_authorizer_connect()


def on_connection_interrupted(connection, error, **kwargs):
    # Callback when connection is accidentally lost.
    print("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    # Callback when an interrupted connection is re-established.
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':
    # Create MQTT connection with a custom authorizer
    mqtt_connection = mqtt_connection_builder.direct_with_custom_authorizer(
        endpoint=cmdData.input_endpoint,
        auth_username=cmdData.input_custom_auth_username,
        auth_authorizer_name=cmdData.input_custom_authorizer_name,
        auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
        auth_password=cmdData.input_custom_auth_password,
        auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
        auth_token_value=cmdData.input_custom_authorizer_token_value,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30)

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
