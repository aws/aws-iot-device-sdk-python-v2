# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io
from awsiot import mqtt_connection_builder
from utils.command_line_utils import CommandLineUtils

# This sample is similar to `samples/basic_connect.py` but the private key
# for mutual TLS is stored on a PKCS#11 compatible smart card or
# Hardware Security Module (HSM).
#
# See `samples/README.md` for instructions on setting up your PKCS#11 device
# to run this sample.
#
# WARNING: Unix only. Currently, TLS integration with PKCS#11 is only available on Unix devices.

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_pkcs11_connect()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


if __name__ == '__main__':

    print(f"Loading PKCS#11 library '{cmdData.input_pkcs11_lib_path}' ...")
    pkcs11_lib = io.Pkcs11Lib(
        file=cmdData.input_pkcs11_lib_path,
        behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
    print("Loaded!")

    pkcs11_slot_id = None
    if (cmdData.input_pkcs11_slot_id):
        pkcs11_slot_id = int(cmdData.input_pkcs11_slot_id)

    # Create MQTT connection
    mqtt_connection = mqtt_connection_builder.mtls_with_pkcs11(
        pkcs11_lib=pkcs11_lib,
        user_pin=cmdData.input_pkcs11_user_pin,
        slot_id=pkcs11_slot_id,
        token_label=cmdData.input_pkcs11_token_label,
        private_key_label=cmdData.input_pkcs11_key_label,
        cert_filepath=cmdData.input_cert,
        endpoint=cmdData.input_endpoint,
        port=cmdData.input_port,
        ca_filepath=cmdData.input_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30)

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
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
