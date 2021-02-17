# Sample apps for the AWS IoT Device SDK v2 for Python

* [pubsub](#pubsub)
* [shadow](#shadow)
* [fleet provisioning](#fleet-provisioning)
* [basic discovery](#basic-discovery)
* [IPC with AWS IoT Greengrass to publish to AWS IoT Core](#ipc-with-aws-iot-greengrass-to-publish-to-aws-iot-core)

## pubsub
This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages
through an MQTT connection. On startup, the device connects to the server,
subscribes to a topic, and begins publishing messages to that topic.
The device should receive those same messages back from the message broker,
since it is subscribed to that same topic.
Status updates are continually printed to the console.

Source: `samples/pubsub.py`

Run the sample like this:
```
python3 pubsub.py --endpoint <endpoint> --root-ca <file> --cert <file> --key <file>
```

Your Thing's
[Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html)
must provide privileges for this sample to connect, subscribe, publish,
and receive.

<details>
<summary>(see sample policy)</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/test/topic"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/test/topic"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
      ]
    }
  ]
}
</pre>
</details>

## shadow

This sample uses the AWS IoT
[Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
Service to keep a property in
sync between device and server. Imagine a light whose color may be changed
through an app, or set by a local user.

Once connected, type a value in the terminal and press Enter to update
the property's "reported" value. The sample also responds when the "desired"
value changes on the server. To observe this, edit the Shadow document in
the AWS Console and set a new "desired" value.

On startup, the sample requests the shadow document to learn the property's
initial state. The sample also subscribes to "delta" events from the server,
which are sent when a property's "desired" value differs from its "reported"
value. When the sample learns of a new desired value, that value is changed
on the device and an update is sent to the server with the new "reported"
value.

Source: `samples/shadow.py`

Run the sample like this:
```
python3 shadow.py --endpoint <endpoint> --root-ca <file> --cert <file> --key <file> --thing-name <name>
```

Your Thing's
[Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html)
must provide privileges for this sample to connect, subscribe, publish,
and receive.

<details>
<summary>(see sample policy)</summary>
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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/get/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/get/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/shadow/update/delta"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/get/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/get/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/update/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/update/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/shadow/update/delta"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
    }
  ]
}
</pre>
</details>

## jobs

This sample uses the AWS IoT
[Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)
Service to receive and execute operations
on the device. Imagine periodic software updates that must be sent to and
executed on devices in the wild.

This sample requires you to create jobs for your device to execute. See
[instructions here](https://docs.aws.amazon.com/iot/latest/developerguide/create-manage-jobs.html).

On startup, the sample tries to start the next pending job execution.
If such a job exists, the sample emulates "doing work" by spawning a thread
that sleeps for several seconds before marking the job as SUCCEEDED. When no
pending job executions exist, the sample sits in an idle state.

The sample also subscribes to receive "Next Job Execution Changed" events.
If the sample is idle, this event wakes it to start the job. If the sample is
already working on a job, it remembers to try for another when it's done.
This event is sent by the service when the current job completes, so the
sample will be continually prompted to try another job until none remain.

Source: `samples/jobs.py`

Run the sample like this:
```
python3 jobs.py --endpoint <endpoint> --root-ca <file> --cert <file> --key <file> --thing-name <name>
```

Your Thing's
[Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html)
must provide privileges for this sample to connect, subscribe, publish,
and receive.
<details>
<summary>(see sample policy)</summary>
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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/start-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/update"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/notify-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/start-next/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/start-next/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/update/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/update/rejected"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/notify-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/start-next/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/start-next/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/*/update/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/*/update/rejected"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
    }
  ]
}
</pre>
</details>

## fleet provisioning

This sample uses the AWS IoT
[Fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)
to provision devices using either a CSR or KeysAndcertificate and subsequently calls RegisterThing.

On startup, the script subscribes to topics based on the request type of either CSR or Keys topics,
publishes the request to corresponding topic and calls RegisterThing.

Source: `samples/fleetprovisioning.py`

Run the sample using createKeysAndCertificate:
```
python3 fleetprovisioning.py --endpoint <endpoint> --root-ca <file> --cert <file> --key <file> --templateName <name> --templateParameters <parameters>
```

Run the sample using createCertificateFromCsr:
```
python3 fleetprovisioning.py --endpoint <endpoint> --root-ca <file> --cert <file> --key <file> --templateName <name> --templateParameters <parameters> --csr <csr file>
```

Your Thing's
[Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html)
must provide privileges for this sample to connect, subscribe, publish,
and receive.

<details>
<summary>(see sample policy)</summary>
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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create/json",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create-from-csr/json",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/provisioning-templates/<b>templatename</b>/provision/json"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive",
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create/json/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create-from-csr/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create-from-csr/json/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/provisioning-templates/<b>templatename</b>/provision/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/provisioning-templates/<b>templatename</b>/provision/json/rejected"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
    }
  ]
}
</pre>
</details>

#### Fleet Provisioning Detailed Instructions

##### Aws Resource Setup
Fleet provisioning requires some additional AWS resources be set up first.  This section documents the steps you need to take to
get the sample up and running.  These steps assume you have the AWS CLI installed and the default user/credentials has
sufficient permission to perform all of the listed operations.  These steps are based on provisioning setup steps
that can be found at [Embedded C SDK Setup](https://docs.aws.amazon.com/freertos/latest/lib-ref/c-sdk/provisioning/provisioning_tests.html#provisioning_system_tests_setup)

First, create the IAM role that will be needed by the fleet provisioning template. Replace `RoleName` with a name of the role you want to create.
<pre>
aws iam create-role \
    --role-name [RoleName] \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"iot.amazonaws.com"}}]}'
</pre>
Next, attach a policy to the role created in the first step. Replace `RoleName` with the name of the role you created previously.
<pre>
aws iam attach-role-policy \
        --role-name [RoleName] \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration
</pre>
Finally, create the template resource which will be used for provisioning by the demo application. This needs to be done only
once.  To create a template, the following AWS CLI command may be used. Replace `TemplateName` with the name of the fleet
provisioning template you want to create. Replace `RoleName` with the name of the role you created previously. Replace
`TemplateJSON` with the template body as a JSON string (containing escape characters). Replace `account` with your AWS
account number.
<pre>
aws iot create-provisioning-template \
        --template-name [TemplateName] \
        --provisioning-role-arn arn:aws:iam::[account]:service-role/[RoleName] \
        --template-body "[TemplateJSON]" \
        --enabled
</pre>
The rest of the instructions assume you have used the following for the template body:
<pre>
{\"Parameters\":{\"DeviceLocation\":{\"Type\":\"String\"},\"AWS::IoT::Certificate::Id\":{\"Type\":\"String\"},\"SerialNumber\":{\"Type\":\"String\"}},\"Mappings\":{\"LocationTable\":{\"Seattle\":{\"LocationUrl\":\"https://example.aws\"}}},\"Resources\":{\"thing\":{\"Type\":\"AWS::IoT::Thing\",\"Properties\":{\"ThingName\":{\"Fn::Join\":[\"\",[\"ThingPrefix_\",{\"Ref\":\"SerialNumber\"}]]},\"AttributePayload\":{\"version\":\"v1\",\"serialNumber\":\"serialNumber\"}},\"OverrideSettings\":{\"AttributePayload\":\"MERGE\",\"ThingTypeName\":\"REPLACE\",\"ThingGroups\":\"DO_NOTHING\"}},\"certificate\":{\"Type\":\"AWS::IoT::Certificate\",\"Properties\":{\"CertificateId\":{\"Ref\":\"AWS::IoT::Certificate::Id\"},\"Status\":\"Active\"},\"OverrideSettings\":{\"Status\":\"REPLACE\"}},\"policy\":{\"Type\":\"AWS::IoT::Policy\",\"Properties\":{\"PolicyDocument\":{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Action\":[\"iot:Connect\",\"iot:Subscribe\",\"iot:Publish\",\"iot:Receive\"],\"Resource\":\"*\"}]}}}},\"DeviceConfiguration\":{\"FallbackUrl\":\"https://www.example.com/test-site\",\"LocationUrl\":{\"Fn::FindInMap\":[\"LocationTable\",{\"Ref\":\"DeviceLocation\"},\"LocationUrl\"]}}}
</pre>
If you use a different body, you may need to pass in different template parameters.
##### Running the sample and provisioning using a certificate-key set from a provisioning claim

To run the provisioning sample, you'll need a certificate and key set with sufficient permissions.  Provisioning certificates are normally
created ahead of time and placed on your device, but for this sample, we will just create them on the fly.  You can also
use any certificate set you've already created if it has sufficient IoT permissions and in doing so, you can skip the step
that calls `create-provisioning-claim`.

We've included a script in the utils folder that creates certificate and key files from the response of calling
`create-provisioning-claim`. These dynamically sourced certificates are only valid for five minutes.  When running the command,
you'll need to substitute the name of the template you previously created, and on Windows, replace the paths with something appropriate.

(Optional) Create a temporary provisioning claim certificate set:
<pre>
aws iot create-provisioning-claim --template-name [TemplateName] | python3 ../utils/parse_cert_set_result.py --path /tmp --filename provision
</pre>

The provisioning claim's cert and key set have been written to `/tmp/provision*`.  Now you can use these temporary keys
to perform the actual provisioning.  If you are not using the temporary provisioning certificate, replace the paths for `--cert`
and `--key` appropriately:

<pre>
python3 fleetprovisioning.py --endpoint [your endpoint]-ats.iot.[region].amazonaws.com --root-ca [pathToRootCA] --cert /tmp/provision.cert.pem --key /tmp/provision.private.key --templateName [TemplateName]--templateParameters "{\"SerialNumber\":\"1\",\"DeviceLocation\":\"Seattle\"}"
</pre>

Notice that we provided substitution values for the two parameters in the template body, `DeviceLocation` and `SerialNumber`.

##### Run the sample using the certificate signing request workflow
To run the sample with this workflow, you'll need to create a certificate signing request.

First create a certificate-key pair:
<pre>
openssl genrsa -out /tmp/deviceCert.key 2048
</pre>

Next create a certificate signing request from it:
<pre>
openssl req -new -key /tmp/deviceCert.key -out /tmp/deviceCert.csr
</pre>

(Optional) As with the previous workflow, we'll create a temporary certificate set from a provisioning claim.  This step can
be skipped if you're using a certificate set capable of provisioning the device:

<pre>
aws iot create-provisioning-claim --template-name [TemplateName] | python3 ../utils/parse_cert_set_result.py --path /tmp --filename provision
</pre>

Finally, supply the certificate signing request while invoking the provisioning sample.  As with the previous workflow, if
using a permanent certificate set, replace the paths specified in the `--cert` and `--key` arguments:
<pre>
python3 fleetprovisioning.py --endpoint [your endpoint]-ats.iot.[region].amazonaws.com --root-ca [pathToRootCA] --cert /tmp/provision.cert.pem --key /tmp/provision.private.key --templateName [TemplateName]--templateParameters "{\"SerialNumber\":\"1\",\"DeviceLocation\":\"Seattle\"}" --csr /tmp/deviceCert.csr
</pre>

## basic discovery

This sample is intended for use directly with the
[Getting Started with AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-gs.html) guide.

## IPC with AWS IoT Greengrass to publish to AWS IoT Core

This sample is intended to be deployed as an AWS IoT Greengrass component and it will publish MQTT messages from the device to AWS IoT Core.

Source: `samples/ipc_greengrass.py`
