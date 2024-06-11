# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
import sys
import time
import traceback
import uuid

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2


def on_message(event):
    try:
        print('Topic: {}'.format(event.binary_message.context.topic))
        message = str(event.binary_message.message, 'utf-8')
        print('Received new message: {}'.format(message))
    except:
        traceback.print_exc()


def main():
    argument_parser = argparse.ArgumentParser(
        description="Run Greengrass subscriber component")
    argument_parser.add_argument(
        "--input_uuid", required=False, help="UUID for unique topic name. UUID will be generated if this option is omit")
    parsed_commands = argument_parser.parse_args()

    input_uuid = parsed_commands.input_uuid if parsed_commands.input_uuid else str(uuid.uuid4())

    try:
        ipc_client = GreengrassCoreIPCClientV2()

        client_device_hello_world_topic = 'clients/+/hello/world/{}'.format(input_uuid)

        # SubscribeToTopic returns a tuple with the response and the operation.
        _, operation = ipc_client.subscribe_to_topic(
            topic=client_device_hello_world_topic, on_stream_event=on_message)
        print('Successfully subscribed to topic: {}'.format(client_device_hello_world_topic))

        # Keep the main thread alive, or the process will exit.
        try:
            while True:
                time.sleep(10)
        except InterruptedError:
            print('Subscribe interrupted.')

        operation.close()
    except Exception:
        print('Exception occurred when using IPC.', file=sys.stderr)
        traceback.print_exc()
        exit(1)

    print("Subscriber done")


if __name__ == "__main__":
    main()
