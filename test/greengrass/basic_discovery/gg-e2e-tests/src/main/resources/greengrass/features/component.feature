Feature: Testing features of Greengrassv2 basic discovery sample

    @testgg
    Scenario: As a developer, I can create a component and deploy it on my device
        Given my device is registered as a Thing
        And my device is running Greengrass
        When I create a Greengrass deployment with components
            | aws.greengrass.clientdevices.Auth            | LATEST           |
            | aws.greengrass.clientdevices.mqtt.Moquette   | LATEST           |
            | aws.greengrass.clientdevices.mqtt.Bridge     | LATEST           |
            | aws.greengrass.clientdevices.IPDetector      | LATEST           |
            | software.amazon.awssdk.sdk-gg-test-discovery | file:recipe.yaml |
        When I update my Greengrass deployment configuration, setting the component aws.greengrass.clientdevices.Auth configuration to:
        """
        {
            "MERGE": {
                "deviceGroups": {
                    "formatVersion": "2021-03-05",
                    "definitions": {
                        "MyDeviceGroup": {
                            "selectionRule": "thingName: CI_Greengrass_Discovery_Thing",
                            "policyName": "MyRestrictivePolicy"
                        }
                    },
                    "policies": {
                        "MyRestrictivePolicy": {
                            "AllowConnect": {
                                "statementDescription": "Allow client devices to connect.",
                                "operations": [
                                    "mqtt:connect"
                                ],
                                "resources": [
                                    "*"
                                ]
                            },
                            "AllowPublish": {
                                "statementDescription": "Allow client devices to publish on topic.",
                                "operations": [
                                    "mqtt:publish"
                                ],
                                "resources": [
                                    "*clients/*/hello/world/*"
                                ]
                            }
                        }
                    }
                }
            }
        }
        """
        When I update my Greengrass deployment configuration, setting the component aws.greengrass.clientdevices.mqtt.Bridge configuration to:
        """
        {
            "MERGE": {
                "mqttTopicMapping": {
                    "HelloWorldCoreMapping": {
                        "topic": "clients/+/hello/world/+",
                        "source": "LocalMqtt",
                        "target": "IotCore"
                    },
                    "HelloWorldPubsubMapping": {
                        "topic": "clients/+/hello/world/+",
                        "source": "LocalMqtt",
                        "target": "Pubsub"
                    }
                }
            }
        }
        """
        And I deploy the Greengrass deployment configuration
        Then the Greengrass deployment is COMPLETED on the device after 300 seconds
        And the software.amazon.awssdk.sdk-gg-test-discovery log on the device contains the line "Successfully subscribed to topic" within 180 seconds
        And the software.amazon.awssdk.sdk-gg-test-discovery log on the device contains the line "Received new message" within 240 seconds
        And the software.amazon.awssdk.sdk-gg-test-discovery log on the device contains the line "disassociated CI_Greengrass_Discovery_Thing" within 260 seconds
