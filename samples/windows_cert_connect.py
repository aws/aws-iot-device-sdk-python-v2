# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt_connection_builder
from uuid import uuid4

# This sample is similar to `samples/basic_connect.py` but the certificate
# for mutual TLS is stored in a Windows certificate store.
#
# See `samples/README.md` for instructions on setting up your PC
# to run this sample.
#
# WARNING: Windows only.

# Parse arguments
import command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("Windows Cert Connect - Make a MQTT connection using Windows Store Certificates.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()


def on_connection_interrupted(connection, error, **kwargs):
    # Callback when connection is accidentally lost.
    print("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    # Callback when an interrupted connection is re-established.
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':
    # Create MQTT connection
    mqtt_connection = mqtt_connection_builder.mtls_with_windows_cert_store_path(
        cert_store_path=cmdUtils.get_command_required("cert"),
        endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
        port=cmdUtils.get_command("port"),
        ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdUtils.get_command("client_id"),
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
