# Shadow Sandbox

[**Return to main sample list**](../README.md)
*__Jump To:__*
* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Walkthrough](#walkthrough)
  * [Initialization](#initialization)
  * [Changing Properties](#changing-properties)
  * [Multiple Properties](#multiple-properties)
  * [Removing Properties](#removing-properties)
  * [Removing a Shadow](#removing-a-shadow)


## Introduction
This is an interactive sample that supports a set of commands that allow you to interact with "classic" (unnamed) shadows of the AWS IoT [Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) Service.

### Commands
Once connected, the sample supports the following shadow-related commands:

* `get` - gets the current full state of the classic (unnamed) shadow.  This includes both a "desired" state component and a "reported" state component.
* `delete` - deletes the classic (unnamed) shadow completely
* `update-desired <desired-state-json-document>` - applies an update to the classic shadow's desired state component.  Properties in the JSON document set to non-null will be set to new values.  Properties in the JSON document set to null will be removed.
* `update-reported <reported-state-json-document>` - applies an update to the classic shadow's reported state component.  Properties in the JSON document set to non-null will be set to new values.  Properties in the JSON document set to null will be removed.

Two additional commands are supported:
* `help` - prints the set of supported commands
* `quit` - quits the sample application

### Prerequisites
Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

<details>
<summary>Sample Policy</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/get",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/delete",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/get/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/delete/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/get/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/delete/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/update/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/*"
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.
* `<thingname>`: The name of your AWS IoT Core thing you want the device connection to be associated with

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `mqtt5-sample-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## Walkthrough

First, from an empty directory, clone the SDK via git:
``` sh
git clone https://github.com/aws/aws-iot-device-sdk-python-v2
```
If not already active, activate the [virtual environment](https://docs.python.org/3/library/venv.html) that will be used to contain Python's execution context.

If the venv does not yet have the device SDK installed, install it:

``` sh
python3 -m pip install awsiotsdk
```

Assuming you are in the SDK root directory, you can now run the shadow sandbox sample:

``` sh
python3 samples/service_clients/shadow.py --cert <path to certificate> --key <path to private key> --endpoint <account-specific broker endpoint> --thing <thing name>
```

The sample also listens to a pair of event streams related to the classic (unnamed) shadow state of your thing, so in addition to responses, you will occasionally see output from these streaming operations as they receive events from the shadow service.

Once successfully connected, you can issue commands.

### Initialization

Start off by getting the shadow state:

```
get
```

If your thing does have shadow state, you will get its current value, which this sample has no control over.  

If your thing does not have any shadow state, you'll get a ResourceNotFound error:

```
Exception: ('get_shadow failure', None, awsiot.iotshadow.V2ErrorResponse(client_token='a8c0465f-e9d3-4a72-bf80-a8e39dd8ba00', code=404, message="No shadow exists with name: 'HelloWorld'", timestamp=None))
```

To create a shadow, you can issue an update call that will initialize the shadow to a starting state:

```
update-reported {"Color":"green"}
```

which will yield output similar to:

```
Received ShadowUpdatedEvent: 
  awsiot.iotshadow.ShadowUpdatedEvent(current=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired=None, reported={'Color': {'timestamp': 1747329779}}), state=awsiot.iotshadow.ShadowState(desired=None, desired_is_nullable=False, reported={'Color': 'green'}, reported_is_nullable=False), version=1), previous=None, timestamp=datetime.datetime(2025, 5, 15, 10, 22, 59))

update-reported response:
  awsiot.iotshadow.UpdateShadowResponse(client_token='1400d004-176a-4639-8378-d1da06aaebe4', metadata=awsiot.iotshadow.ShadowMetadata(desired=None, reported={'Color': {'timestamp': 1747329779}}), state=awsiot.iotshadow.ShadowState(desired=None, desired_is_nullable=False, reported={'Color': 'green'}, reported_is_nullable=False), timestamp=datetime.datetime(2025, 5, 15, 10, 22, 59), version=1)
```

Notice that in addition to receiving a response to the update request, you also receive a `ShadowUpdated` event containing what changed about 
the shadow plus additional metadata (version, update timestamps, etc...).  Every time a shadow is updated, this 
event is triggered.  If you wish to listen and react to this event, use the `create_shadow_updated_stream` API in the shadow client to create a 
streaming operation that converts the raw MQTT publish messages into modeled data that the streaming operation emits via a callback.

Issue one more update to get the shadow's reported and desired states in sync:

```
update-desired {"Color":"green"}
```

yielding output similar to:

```
update-desired response:
  awsiot.iotshadow.UpdateShadowResponse(client_token='15a30d2b-3406-4494-8a75-93bb4314d301', metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329882}}, reported=None), state=awsiot.iotshadow.ShadowState(desired={'Color': 'green'}, desired_is_nullable=False, reported=None, reported_is_nullable=False), timestamp=datetime.datetime(2025, 5, 15, 10, 24, 42), version=2)

<ShadowUpdated event omitted>
```

### Changing Properties
A device shadow contains two independent states: reported and desired.  "Reported" represents the device's last-known local state, while
"desired" represents the state that control application(s) would like the device to change to.  In general, each application (whether on the device or running
remotely as a control process) will only update one of these two state components.  

Let's walk through the multi-step process to coordinate a change-of-state on the device.  First, a control application needs to update the shadow's desired 
state with the change it would like applied:

```
update-desired {"Color":"red"}
```

For our sample, this yields output similar to:

```
Received ShadowUpdatedEvent: 
  awsiot.iotshadow.ShadowUpdatedEvent(current=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}}, reported={'Color': {'timestamp': 1747329779}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red'}, desired_is_nullable=False, reported={'Color': 'green'}, reported_is_nullable=False), version=3), previous=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329882}}, reported={'Color': {'timestamp': 1747329779}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'green'}, desired_is_nullable=False, reported={'Color': 'green'}, reported_is_nullable=False), version=2), timestamp=datetime.datetime(2025, 5, 15, 10, 25, 45))

Received ShadowDeltaUpdatedEvent: 
  awsiot.iotshadow.ShadowDeltaUpdatedEvent(client_token='7ebae3ac-588c-4d73-9c59-59f38b3a0802', metadata={'Color': {'timestamp': 1747329945}}, state={'Color': 'red'}, timestamp=datetime.datetime(2025, 5, 15, 10, 25, 45), version=3)

update-desired response:
  awsiot.iotshadow.UpdateShadowResponse(client_token='7ebae3ac-588c-4d73-9c59-59f38b3a0802', metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}}, reported=None), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red'}, desired_is_nullable=False, reported=None, reported_is_nullable=False), timestamp=datetime.datetime(2025, 5, 15, 10, 25, 45), version=3)
```

The key thing to notice here is that in addition to the update response (which only the control application would see) and the ShadowUpdated event,
there is a new event, ShadowDeltaUpdated, which indicates properties on the shadow that are out-of-sync between desired and reported.  All out-of-sync
properties will be included in this event, including properties that became out-of-sync due to a previous update.

Like the ShadowUpdated event, ShadowDeltaUpdated events can be listened to by creating and configuring a streaming operation, this time by using 
the `create_shadow_delta_updated_stream` API.  Using the `ShadowDeltaUpdatedEvent` events (rather than `ShadowUpdatedEvent`) lets a device focus on just what has 
changed without having to do complex JSON diffs on the full shadow state itself.

Assuming that the change expressed in the desired state is reasonable, the device should apply it internally and then let the service know it
has done so by updating the reported state of the shadow:

```
update-reported {"Color":"red"}
```

yielding

```
Received ShadowUpdatedEvent: 
  awsiot.iotshadow.ShadowUpdatedEvent(current=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}}, reported={'Color': {'timestamp': 1747330109}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red'}, desired_is_nullable=False, reported={'Color': 'red'}, reported_is_nullable=False), version=4), previous=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}}, reported={'Color': {'timestamp': 1747329779}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red'}, desired_is_nullable=False, reported={'Color': 'green'}, reported_is_nullable=False), version=3), timestamp=datetime.datetime(2025, 5, 15, 10, 28, 29))

update-reported response:
  awsiot.iotshadow.UpdateShadowResponse(client_token='a5aad610-0a23-4b46-bf74-575c85caa70d', metadata=awsiot.iotshadow.ShadowMetadata(desired=None, reported={'Color': {'timestamp': 1747330109}}), state=awsiot.iotshadow.ShadowState(desired=None, desired_is_nullable=False, reported={'Color': 'red'}, reported_is_nullable=False), timestamp=datetime.datetime(2025, 5, 15, 10, 28, 29), version=4)
```

Notice that no ShadowDeltaUpdated event is generated because the reported and desired states are now back in sync.  

### Multiple Properties
Not all shadow properties represent device configuration.  To illustrate several more aspects of the Shadow service, let's add a second property to our shadow document, 
starting out in sync (output omitted):

```
update-reported {"Status":"Great"}
```

```
update-desired {"Status":"Great"}
```

Notice that shadow updates work by deltas rather than by complete state changes.  Updating the "Status" property to a value had no effect on the shadow's
"Color" property:

```
get
```

yields

```
get response:
  awsiot.iotshadow.GetShadowResponse(client_token='132f013d-b6f2-482e-a841-3b40e8611791', metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}, 'Status': {'timestamp': 1747330183}}, reported={'Color': {'timestamp': 1747330109}, 'Status': {'timestamp': 1747330176}}), state=awsiot.iotshadow.ShadowStateWithDelta(delta=None, desired={'Color': 'red', 'Status': 'Great'}, reported={'Color': 'red', 'Status': 'Great'}), timestamp=datetime.datetime(2025, 5, 15, 10, 29, 51), version=6)
```

Suppose something goes wrong with the device and its status is no longer "Great"

```
update-reported {"Status":"Awful"}
```

which yields something similar to:

```
Received ShadowUpdatedEvent: 
  awsiot.iotshadow.ShadowUpdatedEvent(current=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}, 'Status': {'timestamp': 1747330183}}, reported={'Color': {'timestamp': 1747330109}, 'Status': {'timestamp': 1747330244}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red', 'Status': 'Great'}, desired_is_nullable=False, reported={'Color': 'red', 'Status': 'Awful'}, reported_is_nullable=False), version=7), previous=awsiot.iotshadow.ShadowUpdatedSnapshot(metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}, 'Status': {'timestamp': 1747330183}}, reported={'Color': {'timestamp': 1747330109}, 'Status': {'timestamp': 1747330176}}), state=awsiot.iotshadow.ShadowState(desired={'Color': 'red', 'Status': 'Great'}, desired_is_nullable=False, reported={'Color': 'red', 'Status': 'Great'}, reported_is_nullable=False), version=6), timestamp=datetime.datetime(2025, 5, 15, 10, 30, 44))

update-reported response:
  awsiot.iotshadow.UpdateShadowResponse(client_token='17c3e551-afd9-4951-bdba-fc9425e86a08', metadata=awsiot.iotshadow.ShadowMetadata(desired=None, reported={'Status': {'timestamp': 1747330244}}), state=awsiot.iotshadow.ShadowState(desired=None, desired_is_nullable=False, reported={'Status': 'Awful'}, reported_is_nullable=False), timestamp=datetime.datetime(2025, 5, 15, 10, 30, 44), version=7)

Received ShadowDeltaUpdatedEvent: 
  awsiot.iotshadow.ShadowDeltaUpdatedEvent(client_token='17c3e551-afd9-4951-bdba-fc9425e86a08', metadata={'Status': {'timestamp': 1747330183}}, state={'Status': 'Great'}, timestamp=datetime.datetime(2025, 5, 15, 10, 30, 44), version=7)
```

Similar to how updates are delta-based, notice how the ShadowDeltaUpdated event only includes the "Status" property, leaving the "Color" property out because it 
is still in sync between desired and reported.

### Removing Properties
Properties can be removed from a shadow by setting them to null.  Removing a property completely would require its removal from both the
reported and desired states of the shadow (output omitted):

```
update-reported {"Status":null}
```

```
update-desired {"Status":null}
```

If you now get the shadow state:

```
get
```

its output yields something like

```
get response:
  awsiot.iotshadow.GetShadowResponse(client_token='3157f35a-f7a7-4ed2-8e2d-eff3fe7f0bff', metadata=awsiot.iotshadow.ShadowMetadata(desired={'Color': {'timestamp': 1747329945}}, reported={'Color': {'timestamp': 1747330109}}), state=awsiot.iotshadow.ShadowStateWithDelta(delta=None, desired={'Color': 'red'}, reported={'Color': 'red'}), timestamp=datetime.datetime(2025, 5, 15, 10, 31, 51), version=9)
```

The Status property has been fully removed from the shadow state.

### Removing a Shadow
To remove a shadow, you must invoke the DeleteShadow API (setting the reported and desired
states to null will only clear the states, but not delete the shadow resource itself).

```
delete
```

yields something like

```
delete response:
  awsiot.iotshadow.DeleteShadowResponse(client_token='31a0b27a-a4b6-4883-afd5-ce485f309926', timestamp=datetime.datetime(2025, 5, 15, 10, 32, 24), version=9)
```

## ⚠️ Usage disclaimer

These code examples interact with services that may incur charges to your AWS account. For more information, see [AWS Pricing](https://aws.amazon.com/pricing/).

Additionally, example code might theoretically modify or delete existing AWS resources. As a matter of due diligence, do the following:

- Be aware of the resources that these examples create or delete.
- Be aware of the costs that might be charged to your account as a result.
- Back up your important data.
