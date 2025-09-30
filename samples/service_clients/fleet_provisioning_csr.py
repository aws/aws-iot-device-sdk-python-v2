# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import iotidentity, mqtt5_client_builder
from awscrt import mqtt5, mqtt_request_response
from concurrent.futures import Future
import json, uuid

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse

parser = argparse.ArgumentParser(
    description="AWS IoT CSR Fleet Provisioning sample application")
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required Arguments
required.add_argument('--endpoint',  metavar="", required=True,
                      help="AWS IoT endpoint to connect to")
required.add_argument('--cert',  metavar="", required=True,
                    help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument('--key',  metavar="", required=True,
                    help="Path to the private key file to use during mTLS connection establishment")
required.add_argument('--template_name',  metavar="", required=True,
                    help="Name of the provisioning template to use")
required.add_argument('--csr_file',  metavar="", required=True,
                    help="Path to a CSR file in PEM format")

# Optional Arguments
optional.add_argument('--template_parameters',  metavar="", required=False,
                    help="JSON map of substitution parameters for the provisioning template")

args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


if __name__ == '__main__':
    with open(args.csr_file, "r") as csr_file:
        csr_data = csr_file.read()

    initial_connection_success = Future()
    def on_lifecycle_connection_success(event: mqtt5.LifecycleConnectSuccessData):
        initial_connection_success.set_result(True)

    def on_lifecycle_connection_failure(event: mqtt5.LifecycleConnectFailureData):
        initial_connection_success.set_exception(Exception("Failed to connect"))

    def on_lifecycle_disconnection(event: mqtt5.LifecycleDisconnectData):
        print("Lifecycle Disconnected with reason code:{}".format(
            event.disconnect_packet.reason_code if event.disconnect_packet else "None"))

    stopped = Future()
    def on_lifecycle_stopped(event: mqtt5.LifecycleStoppedData):
        stopped.set_result(True)

    connect_options=mqtt5.ConnectPacket(
        client_id="mqtt5-sample-" + uuid.uuid4().hex,
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
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        on_lifecycle_disconnection=on_lifecycle_disconnection,
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

    create_certificate_from_csr_response = identity_client.create_certificate_from_csr(iotidentity.CreateCertificateFromCsrRequest(
        certificate_signing_request=csr_data
    )).result()
    print(f"CreateCertificateFromCsr response: {create_certificate_from_csr_response}\n")

    register_thing_request = iotidentity.RegisterThingRequest(
        template_name=args.template_name,
        certificate_ownership_token=create_certificate_from_csr_response.certificate_ownership_token,
    )

    if (args.template_parameters):
        register_thing_request.parameters = json.loads(args.template_parameters.strip())

    register_thing_response = identity_client.register_thing(register_thing_request).result()
    print(f"RegisterThing response: {register_thing_response}\n")

    mqtt5_client.stop()
    stopped.result()
    print("Stopped!")



