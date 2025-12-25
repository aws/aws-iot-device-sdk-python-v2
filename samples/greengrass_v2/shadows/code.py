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
shadow_name = "special_shadow"
shadow = {}


def on_stream_event(message: IoTCoreMessage):
    print(f"Message received:", message)
    reply = json.dumps(
        {
            "pong": "sending back what was received",
            "topic": message.message.topic_name,
            "payload": message.message.payload.decode(),
        }
    )

    print("Sending pong message back:", reply)
    resp = client.publish_to_topic(
        topic_name=message.message.topic_name,
        qos=QOS.AT_LEAST_ONCE,
        payload=reply,
    )
    print(resp)


def main():
    r = client.list_named_shadows_for_thing(thing_name=thing_name)
    if not r.results:
        # named shadow not found, so we have to create it first
        client.update_thing_shadow(
            thing_name=thing_name,
            shadow_name=shadow_name,
            payload=json.dumps(
                {
                    "state": {
                        "reported": {
                            "health": "good",
                        }
                    }
                }
            ),
        )

    # getting the initial shadow document
    p = client.get_thing_shadow(thing_name=thing_name, shadow_name=shadow_name).payload
    shadow = json.loads(p)
    print("Initial shadow:", shadow)

    # doing some useful work, e.g., changing engine speed and reporting the new state
    loop_iteration = 0
    while True:
        loop_iteration += 1
        shadow_update = {
            "state": {
                "reported": {
                    "my_loop_iteration": loop_iteration,
                    "my_time": int(time.time()),
                }
            }
        }
        p = json.dumps(shadow_update).encode()
        print("Updating reported shadow value:", shadow_update)
        p = client.update_thing_shadow(
            thing_name=thing_name, shadow_name=shadow_name, payload=p
        )
        print("Shadow updated:", p)

        time.sleep(5)


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
