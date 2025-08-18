# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

def parse_sample_input():
    parser = argparse.ArgumentParser(
        description="MQTT5 pub/sub sample (mTLS).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--endpoint", required=True, dest="input_endpoint", help="IoT endpoint hostname")
    parser.add_argument("--ca", dest="input_ca", help="Path to optional CA bundle (PEM)")

    parser.add_argument("--custom_auth_username", dest="input_custom_auth_username",
                        help="The name to send when connecting through the custom authorizer (optional)")
    parser.add_argument("--custom_auth_authorizer_name", dest="input_custom_authorizer_name",
                        help="The name of the custom authorizer to connect to (optional but required for everything but custom domains)")
    parser.add_argument("--custom_auth_authorizer_signature", dest="input_custom_authorizer_signature",
                        help="The signature to send when connecting through a custom authorizer (optional)")
    parser.add_argument("--custom_auth_password", dest="input_custom_auth_password",
                        help="The password to send when connecting through a custom authorizer (optional)")
    parser.add_argument("--custom_auth_token_key_name", dest="input_custom_authorizer_token_key_name",
                        help="Key used to extract the custom authorizer token (optional)")
    parser.add_argument("--custom_auth_token_value", dest="input_custom_authorizer_token_value",
                        help="The opaque token value for the custom authorizer (optional)")
    
    parser.add_argument("--use_websockets", dest="input_use_websockets",
                        action="store_const", const=True, default=None,
                        help="Use WebSockets instead of direct TLS")

    # Misc
    parser.add_argument("--client-id", dest="input_clientId",
                        default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}", help="Client ID")
    
    args = parser.parse_args()

    # Validate custom-authorizer inputs:
    # Either provide --custom-auth-username, OR provide signature + token key + token value.
    has_username = bool(args.input_custom_auth_username)
    has_token_triplet = all([
        args.input_custom_authorizer_signature,
        args.input_custom_authorizer_token_key_name,
        args.input_custom_authorizer_token_value,
    ])

    return args

cmdData = parse_sample_input()

# --------------------------------- ARGUMENT PARSING END -----------------------------------------

from awsiot import mqtt5_client_builder
from awscrt import mqtt5
from concurrent.futures import Future

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

    # Create MQTT5 Client with a custom authorizer
    if cmdData.input_use_websockets is None:
        client = mqtt5_client_builder.direct_with_custom_authorizer(
            endpoint=cmdData.input_endpoint,
            ca_filepath=cmdData.input_ca,
            auth_username=cmdData.input_custom_auth_username,
            auth_authorizer_name=cmdData.input_custom_authorizer_name,
            auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
            auth_password=cmdData.input_custom_auth_password,
            auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
            auth_token_value=cmdData.input_custom_authorizer_token_value,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdData.input_clientId)
    else:
        client = mqtt5_client_builder.websockets_with_custom_authorizer(
            endpoint=cmdData.input_endpoint,
            auth_username=cmdData.input_custom_auth_username,
            auth_authorizer_name=cmdData.input_custom_authorizer_name,
            auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
            auth_password=cmdData.input_custom_auth_password,
            auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
            auth_token_value=cmdData.input_custom_authorizer_token_value,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            client_id=cmdData.input_clientId)

    print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")

    client.start()
    future_connection_success.result(TIMEOUT)
    print("Client Connected")

    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")
