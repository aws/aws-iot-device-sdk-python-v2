#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import time
import os
import json

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import QOS, IoTCoreMessage

client = GreengrassCoreIPCClientV2()
thing_name = os.environ["AWS_IOT_THING_NAME"]


def on_stream_event(message: IoTCoreMessage):
    print(f"Message received:", message)
    reply = {
        "pong": "sending back what was received",
        "topic": message.message.topic_name,
        "payload": message.message.payload.decode(),
    }

    print("Sending pong message back:", reply)
    resp = client.publish_to_iot_core(
        topic_name="hello/world/response",
        qos=QOS.AT_LEAST_ONCE,
        payload=json.dumps(reply),
    )
    print(resp)


def main():
    print(f"Running pubsub-cloud sample for thing: {thing_name}")
    topic_name = "hello/world"

    print(f"Subscribing to AWS IoT Core topic {topic_name}")
    resp, op = client.subscribe_to_iot_core(
        topic_name=topic_name,
        qos=QOS.AT_LEAST_ONCE,
        on_stream_event=on_stream_event,
    )
    print(resp, op)

    while True:
        time.sleep(999)  # wait for incoming messages


if __name__ == "__main__":
    # Once we enter here, we know:
    #   * all dependencies are available (imports succeeded)
    #   * IPC Client created
    #   * AWS_IOT_THING_NAME environment variable is available
    # This should be sufficient to consider this component `running` and the deployment will be completed.
    # If any of these failed, the component will be `broken`, and the deployment might roll-back or report the error.
    # Once the component is `running`, we need to try as hard as possible to keep it alive and running.
    while True:
        try:
            main()
        except Exception as e:
            print("ERROR", e)
        time.sleep(5)
