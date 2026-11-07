#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import time
import os
import json

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    QOS,
    JsonMessage,
    PublishMessage,
    SubscriptionResponseMessage,
)

client = GreengrassCoreIPCClientV2()
thing_name = os.environ["AWS_IOT_THING_NAME"]


def on_stream_event(message: SubscriptionResponseMessage):
    print(f"Message received:", message)

    topic = None
    payload = None
    if message.json_message:
        topic = message.json_message.context.topic
        payload = json.dumps(message.json_message.message)
    else:
        topic = message.binary_message.context.topic
        payload = message.binary_message.message.decode()

    reply = {
        "pong": "sending back what was received",
        "topic": topic,
        "payload": payload,
    }

    print("Sending pong message back:", reply)
    resp = client.publish_to_topic(
        topic="hello/world/response",
        publish_message=PublishMessage(json_message=JsonMessage(message=reply)),
    )
    print(resp)


def main():
    print(f"Running pubsub-local sample for thing: {thing_name}")
    topic_name = "hello/world"

    print(f"Subscribing to local topic {topic_name}")
    resp, op = client.subscribe_to_topic(
        topic=topic_name,
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
