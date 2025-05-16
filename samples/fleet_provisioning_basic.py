# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5, mqtt_request_response
from awsiot import iotidentity, mqtt5_client_builder
from concurrent.futures import Future
import argparse
import json
import uuid


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="AWS IoT Basic Fleet Provisioning sample application")
    parser.add_argument('--endpoint', required=True, help="AWS IoT endpoint to connect to")
    parser.add_argument('--cert', required=True,
                        help="Path to the certificate file to use during mTLS connection establishment")
    parser.add_argument('--key', required=True,
                        help="Path to the private key file to use during mTLS connection establishment")
    parser.add_argument('--template_name', required=True,
                        help="Name of the provisioning template to use")
    parser.add_argument('--template_parameters', required=False,
                        help="JSON map of substitution parameters for the provisioning template")

    args = parser.parse_args()

    initial_connection_success = Future()
    def on_lifecycle_connection_success(event: mqtt5.LifecycleConnectSuccessData):
        initial_connection_success.set_result(True)

    def on_lifecycle_connection_failure(event: mqtt5.LifecycleConnectFailureData):
        initial_connection_success.set_exception(Exception("Failed to connect"))

    stopped = Future()
    def on_lifecycle_stopped(event: mqtt5.LifecycleStoppedData):
        stopped.set_result(True)

    connect_options=mqtt5.ConnectPacket(
        client_id="test-" + uuid.uuid4().hex,
    )

    # Create a mqtt5 connection from the command line data
    mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint=args.endpoint,
        port=8883,
        connect_options=connect_options,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        clean_session=True,
        keep_alive_secs=1200,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_stopped=on_lifecycle_stopped)

    mqtt5_client.start()

    rr_options = mqtt_request_response.ClientOptions(
        max_request_response_subscriptions = 2,
        max_streaming_subscriptions = 0,
        operation_timeout_in_seconds = 30,
    )
    identity_client = iotidentity.IotIdentityClientV2(mqtt5_client, rr_options)

    initial_connection_success.result()
    print("Connected!\n")

    create_keys_response = identity_client.create_keys_and_certificate(iotidentity.CreateKeysAndCertificateRequest()).result()
    print(f"CreateKeysAndCertificate response: {create_keys_response}\n")

    register_thing_request = iotidentity.RegisterThingRequest(
        template_name=args.template_name,
        certificate_ownership_token=create_keys_response.certificate_ownership_token,
    )

    if (args.template_parameters):
        register_thing_request.parameters = json.loads(args.template_parameters.strip())

    register_thing_response = identity_client.register_thing(register_thing_request).result()
    print(f"RegisterThing response: {register_thing_response}\n")

    mqtt5_client.stop()
    stopped.result()
    print("Stopped!")



