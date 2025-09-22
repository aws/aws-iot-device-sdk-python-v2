# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import iotshadow, mqtt5_client_builder
from awscrt import mqtt5, mqtt_request_response
from concurrent.futures import Future
from dataclasses import dataclass
from typing import Optional
import awsiot, json, sys

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse

parser = argparse.ArgumentParser(
    description="AWS IoT Shadow sandbox application")
required = parser.add_argument_group("required arguments")

# Required Arguments
required.add_argument('--endpoint',  metavar="", required=True,
                      help="AWS IoT endpoint to connect to")
required.add_argument('--cert',  metavar="", required=True,
                    help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument('--key',  metavar="", required=True,
                    help="Path to the private key file to use during mTLS connection establishment")
required.add_argument('--thing',  metavar="", required=True,
                    help="Name of the IoT thing to interact with")

args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


@dataclass
class SampleContext:
    shadow_client: 'iotshadow.IotShadowClientV2'
    thing: 'str'
    updated_stream: 'Optional[mqtt_request_response.StreamingOperation]' = None
    delta_updated_stream: 'Optional[mqtt_request_response.StreamingOperation]' = None

def print_help():
    print("Shadow Sandbox\n")
    print("Commands:")
    print("  get - gets the current value of the IoT thing's shadow")
    print("  delete - deletes the IoT thing's shadow")
    print("  update-desired <state-as-JSON> - updates the desired state of the IoT thing's shadow.  If the shadow does not exist, it will be created.")
    print("  update-reported <state-as-JSON> - updates the reported state of the IoT thing's shadow.  If the shadow does not exist, it will be created.")
    print("  quit - quits the sample application\n")
    pass

def handle_get(context : SampleContext):
    request = iotshadow.GetShadowRequest(thing_name = context.thing)
    response = context.shadow_client.get_shadow(request).result()
    print(f"get response:\n  {response}\n")
    pass

def handle_delete(context : SampleContext):
    request = iotshadow.DeleteShadowRequest(thing_name = context.thing)
    response = context.shadow_client.delete_shadow(request).result()
    print(f"delete response:\n  {response}\n")

def handle_update_desired(context : SampleContext, line: str):
    request = iotshadow.UpdateShadowRequest(thing_name=context.thing)
    request.state = iotshadow.ShadowState(desired=json.loads(line.strip()))

    response = context.shadow_client.update_shadow(request).result()
    print(f"update-desired response:\n  {response}\n")

def handle_update_reported(context : SampleContext, line: str):
    request = iotshadow.UpdateShadowRequest(thing_name=context.thing)
    request.state = iotshadow.ShadowState(reported=json.loads(line.strip()))

    response = context.shadow_client.update_shadow(request).result()
    print(f"update-reported response:\n  {response}\n")

def handle_input(context : SampleContext, line: str):
    words = line.strip().split(" ", 1)
    command = words[0]

    if command == "quit":
        return True
    elif command == "get":
        handle_get(context)
    elif command == "delete":
        handle_delete(context)
    elif command == "update-desired":
        handle_update_desired(context, words[1])
    elif command == "update-reported":
        handle_update_reported(context, words[1])
    else:
        print_help()

    return False

if __name__ == '__main__':
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

    # Create a mqtt5 connection from the command line data
    mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint=args.endpoint,
        port=8883,
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
        max_streaming_subscriptions = 2,
        operation_timeout_in_seconds = 30,
    )
    shadow_client = iotshadow.IotShadowClientV2(mqtt5_client, rr_options)

    initial_connection_success.result()
    print("Connected!")

    def shadow_updated_callback(event: iotshadow.ShadowUpdatedEvent):
        print(f"Received ShadowUpdatedEvent: \n  {event}\n")

    updated_stream = shadow_client.create_shadow_updated_stream(iotshadow.ShadowUpdatedSubscriptionRequest(thing_name=args.thing), awsiot.ServiceStreamOptions(shadow_updated_callback))
    updated_stream.open()

    def shadow_delta_updated_callback(event: iotshadow.ShadowDeltaUpdatedEvent):
        print(f"Received ShadowDeltaUpdatedEvent: \n  {event}\n")

    delta_updated_stream = shadow_client.create_shadow_delta_updated_stream(iotshadow.ShadowDeltaUpdatedSubscriptionRequest(thing_name=args.thing), awsiot.ServiceStreamOptions(shadow_delta_updated_callback))
    delta_updated_stream.open()

    context = SampleContext(shadow_client, args.thing, updated_stream, delta_updated_stream)

    for line in sys.stdin:
        try:
            if handle_input(context, line):
                break

        except Exception as e:
            print(f"Exception: {e}\n")

    mqtt5_client.stop()
    stopped.result()
    print("Stopped!")



