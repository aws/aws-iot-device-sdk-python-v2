# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, http, auth
from uuid import uuid4
from awsiot import mqtt_connection_builder

# This sample shows how to create a MQTT connection using X509 files to connect.
# This sample is intended to be used as a reference for making MQTT connections via X509.

# Parse arguments
import utils.command_line_utils as command_line_utils
cmdUtils = command_line_utils.CommandLineUtils("X509 Connect - Make a MQTT connection using X509.")
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
    print(f"Connection interrupted. error: {error}")

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")


if __name__ == '__main__':

    ############################################################
    # Pull data from the command line
    ############################################################
    input_endpoint = cmdUtils.get_command_required("endpoint")
    input_signing_region = cmdUtils.get_command_required("signing_region")
    input_ca_file = cmdUtils.get_command("ca_file")
    input_client_id = cmdUtils.get_command_required("client_id")

    input_proxy_host = cmdUtils.get_command("proxy_host")
    input_proxy_port = cmdUtils.get_command("proxy_port")

    input_x509_endpoint = cmdUtils.get_command_required("x509_endpoint")
    input_x509_thing_name = cmdUtils.get_command_required("x509_thing_name")
    input_x509_role_alias = cmdUtils.get_command_required("x509_role_alias")
    input_x509_cert = cmdUtils.get_command_required("x509_cert")
    input_x509_key = cmdUtils.get_command_required("x509_key")
    input_x509_ca_file = cmdUtils.get_command("x509_ca_file")

    ############################################################
    # Set up and create the MQTT connection
    ############################################################

    # Set up the config needed to make a MQTT connection

    proxy_options = None
    if input_proxy_host is not None and input_proxy_port is not None:
        proxy_options = http.HttpProxyOptions(
            host_name=input_proxy_host,
            port=input_proxy_port)

    x509_tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(input_x509_cert, input_x509_key)
    x509_tls_options.ca_dirpath = input_x509_ca_file
    x509_tls_context = io.ClientTlsContext(x509_tls_options)

    x509_provider = auth.AwsCredentialsProvider.new_x509(
        endpoint=input_x509_endpoint,
        thing_name=input_x509_thing_name,
        role_alias=input_x509_role_alias,
        tls_ctx=x509_tls_context,
        http_proxy_options=proxy_options
    )

    # Create the MQTT connection from the configuration

    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=input_endpoint,
        region=input_signing_region,
        credentials_provider=x509_provider,
        http_proxy_options=proxy_options,
        ca_filepath=input_ca_file,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=input_client_id,
        clean_session=False,
        keep_alive_secs=30)

    ############################################################
    # Use the MQTT connection to connect and disconnect
    ############################################################

    if not is_ci:
        print (f"Connecting to {input_endpoint} with client ID '{input_client_id}'...")
    else:
        print("Connecting to endpoint with client ID")

    # Connect
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
