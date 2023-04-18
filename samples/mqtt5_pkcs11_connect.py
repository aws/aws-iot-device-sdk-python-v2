# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5, io
from awsiot import mqtt5_client_builder
from concurrent.futures import Future
from utils.command_line_utils import CommandLineUtils

TIMEOUT = 100

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_mqtt5_pkcs11_connect()

future_stopped = Future()
future_connection_success = Future()

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

    print(f"Loading PKCS#11 library '{cmdData.input_pkcs11_lib_path}' ...")
    pkcs11_lib = io.Pkcs11Lib(
        file=cmdData.input_pkcs11_lib_path,
        behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
    print("Loaded!")

    pkcs11_slot_id = None
    if (cmdData.input_pkcs11_slot_id is not None):
        pkcs11_slot_id = int(cmdData.input_pkcs11_slot_id)

    # Create MQTT5 client
    client = mqtt5_client_builder.mtls_with_pkcs11(
        pkcs11_lib=pkcs11_lib,
        user_pin=cmdData.input_pkcs11_user_pin,
        slot_id=pkcs11_slot_id,
        token_label=cmdData.input_pkcs11_token_label,
        private_key_label=cmdData.input_pkcs11_key_label,
        cert_filepath=cmdData.input_cert,
        endpoint=cmdData.input_endpoint,
        port=cmdData.input_port,
        ca_filepath=cmdData.input_ca,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        client_id=cmdData.input_clientId)

    print("MQTT5 Client Created")

    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Clint Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
