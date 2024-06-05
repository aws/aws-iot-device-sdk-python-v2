Feature: Testing features of Greengrassv2 IPC sample

    @testgg
    Scenario: As a developer, I can create a component and deploy it on my device
        Given my device is registered as a Thing
        And my device is running Greengrass
        When I create a Greengrass deployment with components
            | software.amazon.awssdk.sdk-gg-ipc | file:recipe.yaml |
        And I deploy the Greengrass deployment configuration
        Then the Greengrass deployment is COMPLETED on the device after 180 seconds
        And the software.amazon.awssdk.sdk-gg-ipc log on the device contains the line "Successfully published message" within 20 seconds
