# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5
from concurrent.futures import Future
from utils.command_line_utils import CommandLineUtils

TIMEOUT = 100

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_mqtt5_custom_authorizer_connect()

future_stopped = Future()
future_connection_success = Future()

# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


if __name__ == '__main__':

    # Create MQTT5 Client with a custom authorizer
    if cmdData.input_use_websockets is None:
        client = mqtt5_client_builder.direct_with_custom_authorizer(
            endpoint=cmdData.input_endpoint,
            ca_filepath=cmdData.input_ca,
            auth_username=cmdData.input_custom_auth_username,
            auth_authorizer_name=cmdData.input_custom_authorizer_name,
            auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
            auth_password=cmdData.input_custom_auth_password,
            auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
            auth_token_value=cmdData.input_custom_authorizer_token_value,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdData.input_clientId)
    else:
        client = mqtt5_client_builder.websockets_with_custom_authorizer(
            endpoint=cmdData.input_endpoint,
            auth_username=cmdData.input_custom_auth_username,
            auth_authorizer_name=cmdData.input_custom_authorizer_name,
            auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
            auth_password=cmdData.input_custom_auth_password,
            auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
            auth_token_value=cmdData.input_custom_authorizer_token_value,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdData.input_clientId)

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Client Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
