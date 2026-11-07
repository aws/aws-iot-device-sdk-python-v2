# Greengrass V2 samples using AWS IoT Device SDK v2 for Python

You can find the full API documentation for the Greengrass V2 IPC interface using the Python SDK here: https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/greengrasscoreipc.html

## Sample: Low-Level IPC

Folder: `low_level_ipc/`

Once installed and running, this sample publishes messages to AWS IoT Core. It uses the low-level Greengrass v2 [Inter-Process-Communication API](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html).

See the other samples for higher-level APIs to reduce the amount of code you have to write and maintain.

## Sample: Publish/Subscribe to the cloud with AWS IoT Core

Folder: `pubsub_cloud`

Once installed and running, this sample subscribes to the `hello/world` topic. You can use the [MQTT Test Client](https://console.aws.amazon.com/iot/home#/test) to publish a message to this topic, while also subscribing to `hello/world/response` in the MQTT Test Client. The Greengrass device will receive the message and reply back on the response topic.

## Sample: Public/Subscribe on the local device between Greengrass components

Folder: `pubsub_local`

Once installed and running, this sample subscribes to the `hello/world` topic. You can use a second component to publish a message and receive a reply message on the `hello/world/response` topic. These messages are **not** sent to AWS IoT Core (the cloud). This pub/sub mechanism is only connecting different components running on the same Greengrass device. You can use the Greegrass CLI to publish or subscribe to these local topics:

* `greengrass-cli pubsub sub --topic hello/world/response`
* `greengrass-cli pubsub pub --topic hello/world --message Hi!`

## Sample: Shadow Management

Folder: `shadows`

Once installed and running, this sample will retrieve a named shadow `special_shadow` when the component first starts executing, and then periodically update the shadow document with a new reported state every few seconds.

This component depends on the [AWS-provided ShadowManager component](https://docs.aws.amazon.com/greengrass/v2/developerguide/shadow-manager-component.html#shadow-manager-component-configuration). You [need to configure](https://docs.aws.amazon.com/greengrass/v2/developerguide/shadow-manager-component.html#shadow-manager-component-configuration) it to synchronize named shadows from the local device to the cloud:

```yaml
strategy:
    type: realTime
synchronize:
    coreThing:
    namedShadows:
        - special_shadow
    direction: betweenDeviceAndCloud
```

## Sample: Deployment Configuration

Folder: `deployment_configuration`

Once installed and running, this sample will retrieve the component's deployment configuration and start a web server based on the provided parameters. Re-deploying with different parameters will update the component and upon restart of the Python process, it will start the web server based on these new parameters.

## Deployment Helpers

Deploy component locally using Greengrass CLI:

```bash
func gg_deploy() {
    COMPONENT_NAME=$(sed -nr 's/ComponentName: ([a-zA-Z.-_]+)/\1/p' recipe.yaml)
    COMPONENT_VERSION=$(sed -nr 's/ComponentVersion: (.+)/\1/p' recipe.yaml | tr -d '"' | tr -d "'")
    
    mkdir -p build/artifacts/$COMPONENT_NAME/$COMPONENT_VERSION/
    command cp code.py build/artifacts/$COMPONENT_NAME/$COMPONENT_VERSION/
    
    mkdir -p build/recipes/
    command cp recipe.yaml build/recipes/$COMPONENT_NAME.yaml

    RECIPES=$PWD/build/recipes
    ARTIFACTS=$PWD/build/artifacts
    sudo /greengrass/v2/bin/greengrass-cli deployment create \
        --recipeDir=$RECIPES \
        --artifactDir=$ARTIFACTS \
        --merge=$COMPONENT_NAME=$COMPONENT_VERSION
}

func gg_remove() {
    COMPONENT_NAME=$(sed -nr 's/ComponentName: ([a-zA-Z.-_]+)/\1/p' recipe.yaml)
    sudo /greengrass/v2/bin/greengrass-cli deployment create \
        --recipeDir=$RECIPES \
        --artifactDir=$ARTIFACTS \
        --remove=$COMPONENT_NAME
}
```
