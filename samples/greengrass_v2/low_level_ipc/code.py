#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import json
import time
import os
import random

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

ipc_client = awsiot.greengrasscoreipc.connect()
thing_name = os.environ["AWS_IOT_THING_NAME"]


def send_telemetry():
    telemetry_data = {
        "timestamp": int(time.time()),
        "battery_state_of_charge": random.random() * 99.9,
        "location": {
            "longitude": 48.15743 + random.random() / 10.0,
            "latitude": 11.57549 + random.random() / 10.0,
        },
    }

    op = ipc_client.new_publish_to_iot_core()
    op.activate(
        model.PublishToIoTCoreRequest(
            topic_name=f"my/iot/{thing_name}/telemetry",
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        )
    )
    try:
        result = op.get_response().result(timeout=5.0)
        print("successfully published message:", result)
    except Exception as e:
        print("failed to publish message:", e)


def main():
    while True:
        send_telemetry()
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
