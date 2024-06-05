# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

"""
This sample uses AWS IoT Greengrass v2 to publish messages from the device to
the AWS IoT Core MQTT broker.

This example can be deployed as Greengrass v2 component and it will start
publishing telemetry data as MQTT messages in periodic intervals. The IPC
integration with Greegrass v2 allows this code to run without additional IoT
certificates or secrets, because it directly communicates with Greengrass Core
on the device.

See this page for more information on Greengrass v2 components:
https://docs.aws.amazon.com/greengrass/v2/developerguide/create-components.html

See this page for more information on IPC in Greengrass v2:
https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html

"""

import json
import time
import os
import sys

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    try:
        print("Connecting to Greengrass...")
        ipc_client = awsiot.greengrasscoreipc.connect()

        for i in range(0, 10):
            telemetry_data = {
                "timestamp": int(round(time.time() * 1000)),
                "battery_state_of_charge": 42.5,
                "location": {
                    "longitude": 48.15743,
                    "latitude": 11.57549,
                },
            }

            op = ipc_client.new_publish_to_iot_core()
            op.activate(model.PublishToIoTCoreRequest(
                topic_name="my/iot/{}/telemetry".format(os.getenv("AWS_IOT_THING_NAME")),
                qos=model.QOS.AT_LEAST_ONCE,
                payload=json.dumps(telemetry_data).encode(),
            ))
            try:
                result = op.get_response().result(timeout=5.0)
                print("Successfully published message: {}".format(result))
            except Exception as e:
                print("Failed to publish message: {}".format(e))
                sys.exit(1)

    except Exception as e:
        print("Sample failed: {}".format(e))
        sys.exit(1)
