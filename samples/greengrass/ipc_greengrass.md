# Greengrass IPC

[**Return to main sample list**](./README.md)

This sample uses [AWS IoT Greengrass V2](https://docs.aws.amazon.com/greengrass/index.html) to publish messages from the Greengrass device to the AWS IoT MQTT broker.

This sample can be deployed as a Greengrass V2 component and it will publish 10 MQTT messages over the course of 10 seconds. The IPC integration with Greengrass V2 allows this code to run without additional IoT certificates or secrets, because it directly communicates with the Greengrass core running on the device. As such, to run this sample you need Greengrass Core running.

Some Greengrass references:

* See this page for more information on Greengrass v2 components: https://docs.aws.amazon.com/greengrass/v2/developerguide/create-components.html
* See this page for more information on IPC in Greengrass v2: https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html
* See this page for more information on how to make a local deployment: https://docs.aws.amazon.com/greengrass/v2/developerguide/test-components.html

## How to run

To run the sample, create a new AWS IoT Greengrass component and deploy it to your device with the following recipe snippet to allow your device to publish to AWS IoT Core:

<details>

```yaml
  ---
  RecipeFormatVersion: "2020-01-25"
  ComponentName: "GreengrassIPC"
  ComponentVersion: "1.0.0"
  ComponentDescription: "IPC Greengrass sample."
  ComponentPublisher: "<ComponentPublisher>"
  ComponentConfiguration:
  DefaultConfiguration:
      accessControl:
      aws.greengrass.ipc.mqttproxy:
          software.amazon.awssdk.iotdevicesdk.GreengrassIPC:1:
          policyDescription: "Allows access to publish to all AWS IoT Core topics. For demonstration only - use best practices in a real application"
          operations:
              - aws.greengrass#PublishToIoTCore
          resources:
              - "*"
  Manifests:
  - Platform:
      os: all
      Artifacts:
      - URI: "<S3 Bucket URL>/GreengrassIPC/1.0.0/GreengrassIPC.zip"
      Lifecycle:
          RequiresPrivilege: true
          Run: "python3 -u {artifacts:path}/GreengrassIPC/main.py "
```

Replace the following with your information:
 * `<ComponentPublisher>` with the name you wish to publish your component under.
 * `<S3 Bucket URL>` with the S3 bucket URL for your account to store your Greengrass components under

You can add the following to the recipe `Manifest` snippet to install Python and `AWS IoT Device SDK v2 for Python` as a dependency on Linux:

```yaml
...
Manifests:
  - Platform:
      ...
      Lifecycle:
          Install:
            RequiresPrivilege: true
            Script: "apt-get update --quiet && apt-get --yes install python3 python3-pip && pip3 install awsiotsdk"
          ...
```

</details>
<br />

As an example, you could use the following `gdk-config.json` below in your component with this sample and the recipe yaml shown above:
<details>

```json
  {
  "component": {
      "software.amazon.awssdk.iotdevicesdk.GreengrassIPC": {
      "author": "<ComponentPublisher>",
      "version": "1.0.0",
      "build": {
          "build_system": "zip"
      },
      "publish": {
          "bucket": "<S3 Bucket URL>",
          "region": "<Region>"
      }
      }
  },
  "gdk_version": "1.0.0"
  }
```

Replace the following with your information:
 * `<ComponentPublisher>` with the name you wish to publish your component under.
 * `<S3 Bucket URL>` with the S3 bucket URL for your account to store your Greengrass components under.
 * `<Region>` the region of your S3 bucket and Greengrass device.

</details>
<br />

Note that you will need to have the Python V2 SDK installed on the Greengrass device in order to compile the sample on the Greengrass device.
