# Fleet provisioning MQTT5

[**Return to main sample list**](./README.md)

This sample uses the AWS IoT [Fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html) to provision devices using either a CSR or Keys-And-Certificate and subsequently calls RegisterThing. This allows you to create new AWS IoT Core things using a Fleet Provisioning Template.

On startup, the script subscribes to topics based on the request type of either CSR or Keys topics, publishes the request to corresponding topic and calls RegisterThing.

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

<details>
<summary>(see sample policy)</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create/json",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/certificates/create-from-csr/json",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/provisioning-templates/<b>templatename</b>/provision/json"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:Receive"
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
      "Action": [
        "iot:Subscribe"
      ],
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create/json/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create-from-csr/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create-from-csr/json/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/provisioning-templates/<b>templatename</b>/provision/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/provisioning-templates/<b>templatename</b>/provision/json/rejected"
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

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.
* `<templatename>`: The name of your AWS Fleet Provisioning template you want to use to create new AWS IoT Core Things.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

There are many different ways to run the Fleet Provisioning sample because of how many different ways there are to setup a Fleet Provisioning template in AWS IoT Core. **The easiest and most common way is to run the sample with the following**:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 fleetprovisioning_mqtt5.py --endpoint <endpoint> --cert <file> --key <file> --template_name <name> --template_parameters <parameters>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 fleetprovisioning_mqtt5.py --endpoint <endpoint> --cert <file> --key <file> --template_name <name> --template_parameters <parameters> --ca_file <file>
```

However, this is just one way using the `CreateKeysAndCertificate` workflow. Below are a detailed list of instructions with the different ways to connect. While the detailed instructions do not show it, you can pass `--ca_file` as needed no matter which way you connect via Fleet Provisioning.

## Service Client Notes
### Difference relative to MQTT311 IoTIdentityClient
The IoTIdentityClient with mqtt5 client is almost identical to the mqtt3 one. The only difference is that you would need setup up a Mqtt5 Client and pass it to the IotIdentityClient.
For how to setup a Mqtt5 Client, please refer to [MQTT5 UserGuide](../documents/MQTT5_Userguide.md) and [MQTT5 PubSub Sample](./mqtt5_pubsub.py)

<table>
<tr>
<th>Create a IoTIdentityClient with Mqtt5</th>
<th>Create a IoTIdentityClient with Mqtt311</th>
</tr>
<tr>
<td>

```python
  # Create a Mqtt5 Client
  mqtt5_client = mqtt5_client_builder.mtls_from_path(
          endpoint,
          port,
          cert_filepath,
          pri_key_filepath,
          ca_filepath,
          client_id,
          clean_session,
          keep_alive_secs,
          http_proxy_options,
          on_lifecycle_connection_success,
          on_lifecycle_stopped)

  # Create the Identity Client from Mqtt5 Client
  identity_client = iotidentity.IotIdentityClient(mqtt5_client)
```

</td>
<td>

```python
    # Create a Mqtt311 Connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint,
        port,
        cert_filepath,
        pri_key_filepath,
        ca_filepath,
        client_id,
        clean_session,
        keep_alive_secs,
        http_proxy_options)

    # Create the Identity Client from Mqtt311 Connection
    identity_client = iotidentity.IotIdentityClient(mqtt_connection)
```

</td>
</tr>
</table>

### Mqtt5.QoS v.s. Mqtt3.QoS
As the service client interface is unchanged for both Mqtt3 Connection and Mqtt5 Client,the IotIdentityClient will use Mqtt3.QoS instead of Mqtt5.QoS even with a Mqtt5 Client. You could use mqtt3.QoS.to_mqtt5() and mqtt5.QoS.to_mqtt3() to convert the value.


### Fleet Provisioning Detailed Instructions

#### Aws Resource Setup

Fleet provisioning requires some additional AWS resources be set up first. These steps assume you have the [AWS CLI](https://aws.amazon.com/cli/) installed and have your AWS credentials for the AWS CLI setup and with sufficient permissions to perform all of the operations in this guide. For instructions on how to setup AWS CLI, see the following: [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

You will also need Python version 3 installed to be able to run the `parse_cert_set_result.py` file, which is a helper script to make running this sample easier. You can find Python3 installers for your platform on the [Python website](https://www.python.org/).

These steps are based on the provisioning setup steps
that can be found at [Embedded C SDK Setup](https://docs.aws.amazon.com/freertos/latest/lib-ref/c-sdk/provisioning/provisioning_tests.html#provisioning_system_tests_setup).


First, create the IAM role that will be needed by the fleet provisioning template. Replace `<RoleName>` with a name of the role you want to create.

``` sh
aws iam create-role \
    --role-name <RoleName> \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"iot.amazonaws.com"}}]}'
```

This is the IAM role the Fleet Provisioning template will use to create the new AWS IoT things. However, before it can do so, it will need to have a policy attached to it to give the new role permission to perform the operations it needs. To do this, run the following command and replace `<RoleName>` with the name of the role you created in the previous step.

``` sh
aws iam attach-role-policy \
        --role-name <RoleName> \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration
```

The next step is to make a template resource that will be used for provisioning the new AWS IoT Core things. This template tells AWS IoT Core how to setup the new AWS IoT Core Things you create when your Fleet Provisioning role is invoked, setting up material such as the name and tags, for example.

To create a new Fleet Provisioning template, you can use the following AWS CLI command, replacing `<TemplateName>` with the name of the template you wish to create, `<RoleName>` with the name of the role you created two steps prior, and `<Account>` with your AWS IoT Core account number. Finally, make sure to replace `<TemplateJSON>` with a valid JSON document as a single line. An example JSON document is provided further below.

``` sh
aws iot create-provisioning-template \
        --template-name <TemplateName> \
        --provisioning-role-arn arn:aws:iam::<Account>:role/<RoleName> \
        --template-body "<TemplateJSON>" \
        --enabled
```

For the purposes of this sample, the following template JSON document is presumed to be used:

<details>
<summary>(see template body)</summary>

```json
{
  "Parameters": {
    "DeviceLocation": {
      "Type": "String"
    },
    "AWS::IoT::Certificate::Id": {
      "Type": "String"
    },
    "SerialNumber": {
      "Type": "String"
    }
  },
  "Mappings": {
    "LocationTable": {
      "Seattle": {
        "LocationUrl": "https://example.aws"
      }
    }
  },
  "Resources": {
    "thing": {
      "Type": "AWS::IoT::Thing",
      "Properties": {
        "ThingName": {
          "Fn::Join": [
            "",
            [
              "ThingPrefix_",
              {
                "Ref": "SerialNumber"
              }
            ]
          ]
        },
        "AttributePayload": {
          "version": "v1",
          "serialNumber": "serialNumber"
        }
      },
      "OverrideSettings": {
        "AttributePayload": "MERGE",
        "ThingTypeName": "REPLACE",
        "ThingGroups": "DO_NOTHING"
      }
    },
    "certificate": {
      "Type": "AWS::IoT::Certificate",
      "Properties": {
        "CertificateId": {
          "Ref": "AWS::IoT::Certificate::Id"
        },
        "Status": "Active"
      },
      "OverrideSettings": {
        "Status": "REPLACE"
      }
    },
    "policy": {
      "Type": "AWS::IoT::Policy",
      "Properties": {
        "PolicyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "iot:Connect",
                "iot:Subscribe",
                "iot:Publish",
                "iot:Receive"
              ],
              "Resource": "*"
            }
          ]
        }
      }
    }
  },
  "DeviceConfiguration": {
    "FallbackUrl": "https://www.example.com/test-site",
    "LocationUrl": {
      "Fn::FindInMap": [
        "LocationTable",
        {
          "Ref": "DeviceLocation"
        },
        "LocationUrl"
      ]
    }
  }
}
```

</details>

And here is the same JSON document, but as a single line for easier copy-pasting:

<details>
<summary>(see template body)</summary>

``` json
{"Parameters": {"DeviceLocation": {"Type": "String"},"AWS::IoT::Certificate::Id": {"Type": "String"},"SerialNumber": {"Type": "String"}},"Mappings": {"LocationTable": {"Seattle": {"LocationUrl": "https://example.aws"}}},"Resources": {"thing": {"Type": "AWS::IoT::Thing","Properties": {"ThingName": {"Fn::Join": ["",["ThingPrefix_",{"Ref": "SerialNumber"}]]},"AttributePayload": {"version": "v1","serialNumber": "serialNumber"}},"OverrideSettings": {"AttributePayload": "MERGE","ThingTypeName": "REPLACE","ThingGroups": "DO_NOTHING"}},"certificate": {"Type": "AWS::IoT::Certificate","Properties": {"CertificateId": {"Ref": "AWS::IoT::Certificate::Id"},"Status": "Active"},"OverrideSettings": {"Status": "REPLACE"}},"policy": {"Type": "AWS::IoT::Policy","Properties": {"PolicyDocument": {"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": ["iot:Connect","iot:Subscribe","iot:Publish","iot:Receive"],"Resource": "*"}]}}}},"DeviceConfiguration": {"FallbackUrl": "https://www.example.com/test-site","LocationUrl": {"Fn::FindInMap": ["LocationTable",{"Ref": "DeviceLocation"},"LocationUrl"]}}}
```

</details>

You can use this JSON document as the `<TemplateJSON>` in the AWS CLI command. This sample will assume you have used the template JSON above, so you may need to adjust if you are using a different template JSON. Thankfully, all of these steps need to only be done and, now that they are complete, you will need not perform them again.

#### Creating a certificate-key set from a provisioning claim

To run the provisioning sample, you'll need a certificate and key set with sufficient permissions. Provisioning certificates are normally created ahead of time and placed on your device, but for this sample, we will just create them on the fly. This is primarily done for example purposes.

You can also use any certificate set you've already created if it has sufficient IoT permissions. If you wish to do this, you can skip the step that calls `create-provisioning-claim` below and move right to the next step: [Running the sample using a certificate-key set](#running-the-sample-using-a-certificate-key-set)

We've included a script in the utils folder that creates certificate and key files from the response of calling
`create-provisioning-claim`. These dynamically sourced certificates are **only valid for five minutes**. When running the command,
you'll need to substitute the name of the template you previously created. If on Windows, replace the paths with something appropriate.

**Note**: The following assumes you are running this command from the `aws-iot-device-sdk-java-v2` folder, which is the main GitHub folder. If you are running this from another folder (like the `samples/Identity` folder), then you will need to adjust the filepaths accordingly.

```sh
aws iot create-provisioning-claim \
    --template-name <TemplateName> \
    | python3 ./utils/parse_cert_set_result.py \
    --path ./tmp \
    --filename provision
```
* Replace `<TemplateName>` with the name of the Fleet Provisioning template you created earlier.

This will create a certificate and key in the `tmp` folder with file names starting with `provision`. You can now use these temporary keys
to perform the actual provisioning in the section below.

#### Running the sample using a certificate-key set

To run the sample with your certificate and private key, use the following command:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 fleetprovisioning.py --endpoint <endpoint> --cert <file> --key <file> --template_name <name> --template_parameters '{\"SerialNumber\":\"1\",\"DeviceLocation\":\"Seattle\"}'
```

As per normal, replace the `<>` parameters with the proper values. Notice that we provided substitution values for the two parameters in the template body, `DeviceLocation` and `SerialNumber`.

With that, the sample should run and work as expected! You should then find your have a new AWS IoT Core thing!

### Run the sample using the certificate signing request workflow

To run the sample with this workflow, you'll need to create a certificate signing request in addition to the other steps above (creating the role, setting its policy, setting the template JSON, etc).

First create a certificate-key pair:
``` sh
openssl genrsa -out /tmp/deviceCert.key 2048
```

Next create a certificate signing request from it:
``` sh
openssl req -new -key /tmp/deviceCert.key -out /tmp/deviceCert.csr
```

As in the previous workflow, you can [create a temporary certificate set from a provisioning claim](#creating-a-certificate-key-set-from-a-provisioning-claim). Again, this can be skipped if you have a policy and certificate with the proper permissions.

```sh
aws iot create-provisioning-claim \
    --template-name <TemplateName> \
    | python3 ./utils/parse_cert_set_result.py \
    --path ./tmp \
    --filename provision
```
* Replace `<TemplateName>` with the name of the Fleet Provisioning template you created earlier.

Finally, you can also pass the certificate signing request while invoking the Fleet Provisioning sample.

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 fleetprovisioning.py --endpoint <endpoint> --cert <file> --key <file> --template_name <name> --template_parameters '{\"SerialNumber\":\"1\",\"DeviceLocation\":\"Seattle\"}' --csr <path to csr file>
```
