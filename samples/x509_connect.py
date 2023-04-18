# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, http, auth
from awsiot import mqtt_connection_builder
from utils.command_line_utils import CommandLineUtils

# This sample shows how to create a MQTT connection using X509 files to connect.
# This sample is intended to be used as a reference for making MQTT connections via X509.

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_x509_connect()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. error: {error}")

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")


if __name__ == '__main__':

    ############################################################
    # Set up and create the MQTT connection
    ############################################################

    # Set up the config needed to make a MQTT connection

    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    x509_tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(
        cmdData.input_x509_cert, cmdData.input_x509_key)
    x509_tls_options.ca_dirpath = cmdData.input_x509_ca
    x509_tls_context = io.ClientTlsContext(x509_tls_options)

    x509_provider = auth.AwsCredentialsProvider.new_x509(
        endpoint=cmdData.input_x509_endpoint,
        thing_name=cmdData.input_x509_thing_name,
        role_alias=cmdData.input_x509_role,
        tls_ctx=x509_tls_context,
        http_proxy_options=proxy_options
    )

    # Create the MQTT connection from the configuration
    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=cmdData.input_endpoint,
        region=cmdData.input_signing_region,
        credentials_provider=x509_provider,
        http_proxy_options=proxy_options,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30)

    ############################################################
    # Use the MQTT connection to connect and disconnect
    ############################################################

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
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
