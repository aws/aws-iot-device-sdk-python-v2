# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import command_line_utils
from awscrt import mqtt5
from uuid import uuid4
from concurrent.futures import Future

TIMEOUT = 100

# Parse arguments
cmdUtils = command_line_utils.CommandLineUtils("MQTT5 PKCS11 Connect - Make a MQTT5 Client connection using PKCS11.")
cmdUtils.add_common_mqtt5_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command(
    "port",
    "<int>",
    "Connection port. AWS IoT supports 433 and 8883 (optional, default=auto).",
    type=int)
cmdUtils.register_command(
    "client_id",
    "<str>",
    "Client ID to use for MQTT5 connection (optional, default=None).",
    default="test-" + str(uuid4()))
cmdUtils.register_command("pkcs11_lib", "<path>", "Path to PKCS#11 Library", required=True)
cmdUtils.register_command("pin", "<str>", "User PIN for logging into PKCS#11 token.", required=True)
cmdUtils.register_command("token_label", "<str>", "Label of the PKCS#11 token to use (optional).")
cmdUtils.register_command("slot_id", "<int>", "Slot ID containing the PKCS#11 token to use (optional).", False, int)
cmdUtils.register_command("key_label", "<str>", "Label of private key on the PKCS#11 token (optional).")
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

future_stopped = Future()
future_connection_success = Future()
is_ci = cmdUtils.get_command("is_ci", None) != None

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
    print("\nStarting MQTT5 pkcs11 connect Sample\n")

    # Create MQTT5 Client with using PKCS11
    client = cmdUtils.build_pkcs11_mqtt5_client(
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success)
    print("MQTT5 Client Created")

    if is_ci == False:
        print("Connecting to {} with client ID '{}'...".format(
            cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))
    else:
        print("Connecting to endpoint with client ID")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Clint Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
