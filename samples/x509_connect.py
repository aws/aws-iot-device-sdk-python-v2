# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io
from uuid import uuid4

# This sample shows how to create a MQTT connection using X509 files to connect.
# This sample is intended to be used as a reference for making MQTT connections via X509.

# Parse arguments
import utils.command_line_utils as command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("Basic Connect - Make a MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.add_common_x509_commands()
cmdUtils.register_command("signing_region", "<str>",
                          "The signing region used for the websocket signer",
                          True, str)
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()
is_ci = cmdUtils.get_command("is_ci", None) is not None

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':
    # Create a connection using X509 authentication to connect
    # Note: The data for the connection is gotten from cmdUtils.
    # (see build_websocket_x509_mqtt_connection for implementation)
    mqtt_connection = cmdUtils.build_websocket_x509_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    if not is_ci:
        print("Connecting to {} with client ID '{}'...".format(
            cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))
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
