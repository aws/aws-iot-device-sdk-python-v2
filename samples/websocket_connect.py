# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import http, auth
from awsiot import mqtt_connection_builder
from uuid import uuid4

# This sample shows how to create a MQTT connection using websockets.
# This sample is intended to be used as a reference for making MQTT connections.

# Parse arguments
import command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("PubSub - Send and recieve messages through an MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("signing_region", "<str>",
                          "The signing region used for the websocket signer",
                          True, str)
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':
    proxy_options = None
    if cmdUtils.get_command(cmdUtils.m_cmd_proxy_host) and cmdUtils.get_command(cmdUtils.m_cmd_proxy_port):
        proxy_options = http.HttpProxyOptions(
            host_name=cmdUtils.get_command(cmdUtils.m_cmd_proxy_host),
            port=cmdUtils.get_command(cmdUtils.m_cmd_proxy_port))

    credentials_provider = auth.AwsCredentialsProvider.new_default_chain()
    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
        region=cmdUtils.get_command_required("signing_region"),
        credentials_provider=credentials_provider,
        http_proxy_options=proxy_options,
        ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdUtils.get_command_required("client_id"),
        clean_session=False,
        keep_alive_secs=30)

    print("Connecting to {} with client ID '{}'...".format(
        cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
