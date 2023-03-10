# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5
from uuid import uuid4
from concurrent.futures import Future

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

TIMEOUT = 100

# Parse arguments
cmdUtils = command_line_utils.CommandLineUtils(
    "Custom Authorizer Connect - Make a MQTT5 Client connection using a custom authorizer.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.add_common_custom_authorizer_commands()
cmdUtils.register_command("client_id", "<str>",
                          "Client ID to use for MQTT connection (optional, default='test-*').",
                          default="test-" + str(uuid4()))
cmdUtils.register_command("use_websockets", "<str>", "If set, websockets will be used (optional, do not set to use direct MQTT)")
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

future_stopped = Future()
future_connection_success = Future()
is_ci = cmdUtils.get_command("is_ci", None) != None
use_websockets = cmdUtils.get_command("use_websockets", None) != None

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
    if use_websockets == None:
        client = mqtt5_client_builder.direct_with_custom_authorizer(
            endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
            ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
            auth_username=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_username),
            auth_authorizer_name=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_name),
            auth_authorizer_signature=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_signature),
            auth_password=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_password),
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdUtils.get_command("client_id"))
    else:
        client = mqtt5_client_builder.websockets_with_custom_authorizer(
            endpoint=cmdUtils.get_command_required(cmdUtils.m_cmd_endpoint),
            ca_filepath=cmdUtils.get_command(cmdUtils.m_cmd_ca_file),
            auth_username=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_username),
            auth_authorizer_name=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_name),
            auth_authorizer_signature=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_authorizer_signature),
            auth_password=cmdUtils.get_command(cmdUtils.m_cmd_custom_auth_password),
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdUtils.get_command("client_id"))

    if is_ci == False:
        print("Connecting to {} with client ID '{}'...".format(
            cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))
    else:
        print("Connecting to endpoint with client ID")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Client Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
