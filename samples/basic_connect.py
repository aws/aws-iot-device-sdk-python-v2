# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import http
from awsiot import mqtt_connection_builder
from uuid import uuid4

# This sample shows how to create a MQTT connection using a certificate file and key file.
# This sample is intended to be used as a reference for making MQTT connections.

# Parse arguments
import command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("PubSub - Send and recieve messages through an MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command("port", "<int>",
                          "Connection port for direct connection. " +
                          "AWS IoT supports 433 and 8883 (optional, default=8883).",
                          False, int)
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

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
        port=cmdUtils.get_command_required("port"),
        cert_filepath=cmdUtils.get_command_required("cert"),
        pri_key_filepath=cmdUtils.get_command_required("key"),
        ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdUtils.get_command_required("client_id"),
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options)

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
