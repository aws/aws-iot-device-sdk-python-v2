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

To run the sample, create a new AWS IoT Greengrass component and deploy it to
your device with the following recipe snippet to allow your device to publish to
the AWS IoT Core MQTT broker:

```json
...
"ComponentConfiguration": {
  "DefaultConfiguration": {
    "accessControl": {
      "aws.greengrass.ipc.mqttproxy": {
        "Your.Component.Name:mqttproxy:1": {
          "policyDescription": "Allows access to publish to all AWS IoT Core topics.",
          "operations": [
            "aws.greengrass#PublishToIoTCore"
          ],
          "resources": [
            "*"
          ]
        }
      }
    }
  }
},
...
```
(replace `Your.Component.Name` with your component name)

You can use this recipe `Manifest` snippet to install Python and `AWS IoT Device
SDK v2 for Python` as dependency:
```json
...
"Manifests": [{
  ...
  "Lifecycle": {
    "Install": {
      "RequiresPrivilege": true,
      "Script": "apt-get update --quiet && apt-get --yes install python3 python3-pip && pip3 install awsiotsdk"
    },
  ...
```
"""

import json
import time
import os

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    while True:
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
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(5)
