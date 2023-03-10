# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt_connection_builder
from uuid import uuid4

def link_command_line_utils():
    """
    An unfortunate necessary evil: We need to share the command_line_utils.py file across samples
    but also need each sample in its own folder while still being directly executable. Python does
    not like relative imports with non package/module python files, so we make a symlink if possible.
    If it is not possible, we error out and direct where to find the file
    """
    import os, pathlib
    script_folder = pathlib.Path(os.path.abspath(__file__)).parent
    command_line_utils_file = script_folder.joinpath("./command_line_utils.py")
    # Do not create a symlink if the file already exists
    if (command_line_utils_file.exists() and command_line_utils_file.is_file()):
        return
    # If the file does not exist, try to create a symlink to it
    utils_command_line_utils_file = script_folder.parent.joinpath("./utils/command_line_utils.py")
    if (utils_command_line_utils_file.exists() and utils_command_line_utils_file.is_file()):
        command_line_utils_file.symlink_to(utils_command_line_utils_file, False)
        print ("Created symlink to command_line_utils.py for sample to work correctly...")
    else:
        print("Error: Cannot find command_line_utils.py next to script nor in [../utils/command_line_utils.py]!")
        print ("The sample cannot parse command line arguments without this file and therefore cannot run")
        print ("Please place command_line_utils.py next to this script so it can run. You can find command_line_utils.py")
        print ("at the following URL: https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/utils/command_line_utils.py")
        os._exit(1)
link_command_line_utils()
import command_line_utils

# This sample is similar to `samples/basic_connect.py` but it connects
# through a custom authorizer rather than using a key and certificate.

# Parse arguments
cmdUtils = command_line_utils.CommandLineUtils(
    "Custom Authorizer Connect - Make a MQTT connection using a custom authorizer.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.add_common_custom_authorizer_commands()
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()
is_ci = cmdUtils.get_command("is_ci", None) != None


def on_connection_interrupted(connection, error, **kwargs):
    # Callback when connection is accidentally lost.
    print("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    # Callback when an interrupted connection is re-established.
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':

    # Create MQTT connection with a custom authorizer
    mqtt_connection = mqtt_connection_builder.direct_with_custom_authorizer(
        endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
        ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
        auth_username=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_username),
        auth_authorizer_name=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_name),
        auth_authorizer_signature=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_signature),
        auth_password=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_password),
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdUtils.get_command("client_id"),
        clean_session=False,
        keep_alive_secs=30)

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
