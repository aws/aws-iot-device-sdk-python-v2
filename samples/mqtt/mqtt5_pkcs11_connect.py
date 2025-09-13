# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, io
from concurrent.futures import Future

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

parser = argparse.ArgumentParser(
    description="MQTT5 PKCS11 Sample.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required Arguments
required.add_argument("--endpoint", required=True,  metavar="", dest="input_endpoint",
                      help="IoT endpoint hostname")
optional.add_argument("--port", type=int, default=8883,  metavar="", dest="input_port",
                      help="Port (8883 mTLS, 443 ALPN)")
required.add_argument("--cert", required=True,  metavar="", dest="input_cert",
                    help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument("--pkcs11_lib", required=True,  metavar="", dest="input_pkcs11_lib_path",
                      help="Path to PKCS#11 Library")
required.add_argument("--pin", required=True,  metavar="", dest="input_pkcs11_user_pin",
                      help="User PIN for logging into PKCS#11 token")

# Optional Arguments
optional.add_argument("--token_label",  metavar="", dest="input_pkcs11_token_label",
                      help="Label of the PKCS#11 token to use (optional).")
optional.add_argument("--slot_id", type=int, metavar="", dest="input_pkcs11_slot_id",
                      help="Slot ID containing the PKCS#11 token to use (optional).")
optional.add_argument("--key_label",  metavar="", dest="input_pkcs11_key_label",
                      help="Label of private key on the PKCS#11 token (optional).")
optional.add_argument("--ca_file",  metavar="", dest="input_ca",
                      help="Path to optional CA bundle (PEM)")
optional.add_argument("--topic", default="test/topic",  metavar="", dest="input_topic",
                      help="Topic")
optional.add_argument("--message", default="Hello from mqtt5 sample",  metavar="", dest="input_message",
                      help="Message payload")
optional.add_argument("--count", type=int, default=5,  metavar="", dest="input_count",
                    help="Messages to publish (0 = infinite)")
optional.add_argument("--proxy_host",  metavar="", dest="input_proxy_host",
                      help="HTTP proxy host")
optional.add_argument("--proxy_port", type=int, default=0,  metavar="", dest="input_proxy_port",
                      help="HTTP proxy port")
optional.add_argument("--client_id",  metavar="", dest="input_clientId", default=f"test-{uuid.uuid4().hex[:8]}",
                    help="Client ID")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


TIMEOUT = 100

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

    print(f"Loading PKCS#11 library '{args.input_pkcs11_lib_path}' ...")
    pkcs11_lib = io.Pkcs11Lib(
        file=args.input_pkcs11_lib_path,
        behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
    print("Loaded!")

    pkcs11_slot_id = None
    if (args.input_pkcs11_slot_id is not None):
        pkcs11_slot_id = int(args.input_pkcs11_slot_id)

    # Create MQTT5 client
    client = mqtt5_client_builder.mtls_with_pkcs11(
        pkcs11_lib=pkcs11_lib,
        user_pin=args.input_pkcs11_user_pin,
        slot_id=pkcs11_slot_id,
        token_label=args.input_pkcs11_token_label,
        private_key_label=args.input_pkcs11_key_label,
        cert_filepath=args.input_cert,
        endpoint=args.input_endpoint,
        port=args.input_port,
        ca_filepath=args.input_ca,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        client_id=args.input_clientId)

    print("MQTT5 Client Created")

    print(f"Connecting to {args.input_endpoint} with client ID '{args.input_clientId}'...")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Clint Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
