# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import http, auth
from awsiot import mqtt_connection_builder
from utils.command_line_utils import CommandLineUtils

# This sample shows how to create a MQTT connection using websockets.
# This sample is intended to be used as a reference for making MQTT connections.


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

def connection_setup():
    # cmdData is the arguments/input from the command line placed into a single struct for
    # use in this sample. This handles all of the command line parsing, validating, etc.
    # See the Utils/CommandLineUtils for more information.
    cmdData = CommandLineUtils.parse_sample_input_websocket_connect()

    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    # Create a default credentials provider and a MQTT connection from the command line data
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain()
    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=cmdData.input_endpoint,
        region=cmdData.input_signing_region,
        credentials_provider=credentials_provider,
        http_proxy_options=proxy_options,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30)
    return mqtt_connection, cmdData

if __name__ == '__main__':
    mqtt_connection, cmdData = connection_setup()

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID...")

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
