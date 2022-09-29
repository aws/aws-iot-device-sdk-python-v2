# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io
from awsiot import mqtt_connection_builder
from uuid import uuid4

# This sample is similar to `samples/basic_connect.py` but the private key
# for mutual TLS is stored on a PKCS#11 compatible smart card or
# Hardware Security Module (HSM).
#
# See `samples/README.md` for instructions on setting up your PKCS#11 device
# to run this sample.
#
# WARNING: Unix only. Currently, TLS integration with PKCS#11 is only available on Unix devices.

# Parse arguments
import command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("PKCS11 Connect - Make a MQTT connection using PKCS11.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
cmdUtils.register_command("port", "<port>",
                          "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).",
                          type=int)
cmdUtils.register_command("pkcs11_lib", "<path>", "Path to PKCS#11 Library", required=True)
cmdUtils.register_command("pin", "<str>", "User PIN for logging into PKCS#11 token.", required=True)
cmdUtils.register_command("token_label", "<str>", "Label of the PKCS#11 token to use (optional).")
cmdUtils.register_command("slot_id", "<int>", "Slot ID containing the PKCS#11 token to use (optional).", False, int)
cmdUtils.register_command("key_label", "<str>", "Label of private key on the PKCS#11 token (optional).")
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()
is_ci = cmdUtils.get_command("is_ci", None) != None

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':
    # Create a connection using websockets.
    # Note: The data for the connection is gotten from cmdUtils.
    # (see build_pkcs11_mqtt_connection for implementation)
    mqtt_connection = cmdUtils.build_pkcs11_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    if is_ci == False:
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
