# CSR Fleet provisioning

[**Return to main sample list**](../README.md)
*__Jump To:__*
* [Introduction](#introduction)
* [Requirements](#requirements)
* [How To Run](#how-to-run)
* [Fleet Provisioning Detailed Instructions](#fleet-provisioning-detailed-instructions)
  * [Aws Resource Setup](#aws-resource-setup)
  * [Creating a Certificate-key Set from a Provisioning Claim](#creating-a-certificate-key-set-from-a-provisioning-claim)
  * [Create a Certificate Signing Request and Run the Sample](#create-a-certificate-signing-request-and-run-the-sample)

## Introduction
This sample uses the AWS IoT [Fleet provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html) to provision devices using a certificate signing request. This allows you to create new AWS IoT Core things using a Fleet Provisioning Template.

## Requirements
The [IAM Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) attached to your provisioning certificate must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used that will allow this sample to run as intended.

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create-from-csr/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/certificates/create-from-csr/json/rejected",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/provisioning-templates/<b>templatename</b>/provision/json/accepted",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/provisioning-templates/<b>templatename</b>/provision/json/rejected"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/mqtt5-sample-*"
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.
* `<templatename>`: The name of your AWS Fleet Provisioning template you want to use to create new AWS IoT Core Things.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `mqtt5-sample-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

First, from an empty directory, clone the SDK via git:
``` sh
git clone https://github.com/aws/aws-iot-device-sdk-python-v2
```
If not already active, activate the [virtual environment](https://docs.python.org/3/library/venv.html) that will be used to contain Python's execution context.

If the venv does not yet have the device SDK installed, install it:

``` sh
python3 -m pip install awsiotsdk
```

Assuming you are in the SDK root directory, you can now run the CSR fleet provisioning sample:

``` sh
python3 samples/service_clients/fleet_provisioning_csr.py --endpoint <endpoint> --cert <file> --key <file> --csr_file <file> --template_name <template name> --template_parameters <template parameters>
```

## Fleet Provisioning Detailed Instructions

#### Aws Resource Setup

Fleet provisioning requires some additional AWS resources be set up first. These steps assume you have the [AWS CLI](https://aws.amazon.com/cli/) installed and have your AWS credentials for the AWS CLI setup and with sufficient permissions to perform all of the operations in this guide. For instructions on how to setup AWS CLI, see the following: [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

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

#### Creating a Certificate-key Set from a Provisioning Claim

To run the provisioning sample, you'll need a certificate and key set with permissions to perform the provisioning operations. Provisioning certificates are normally created ahead of time and placed on your device, but for this sample, we will just create them on the fly. This is primarily done for example purposes.

You can also use any certificate set you've already created if it has sufficient IoT permissions. If you wish to do this, you can skip the step that calls `create-provisioning-claim` below and move right to the next step: [Running the sample using a certificate-key set](#running-the-sample-using-a-certificate-key-set)

We've included a script in the utils folder that creates certificate and key files from the response of calling
`create-provisioning-claim`. These dynamically sourced certificates are **only valid for five minutes**. When running the command,
you'll need to substitute the name of the template you previously created. If on Windows, replace the paths with something appropriate.

**Note**: The following assumes you are running this command from the `aws-iot-device-sdk-python-v2` folder, which is the main GitHub folder. If you are running this from another folder then you will need to adjust the filepaths accordingly.

```sh
aws iot create-provisioning-claim \
    --template-name <TemplateName> \
    | python3 ./utils/parse_cert_set_result.py \
    --path /tmp \
    --filename provision
```
* Replace `<TemplateName>` with the name of the Fleet Provisioning template you created earlier.

This will create a certificate and key in the `/tmp` folder with file names starting with `provision`. You can now use these temporary keys
to perform the actual provisioning in the section below.

### Create a Certificate Signing Request and Run the Sample

You'll need to create a certificate signing request in addition to the other steps above (creating the role, setting its policy, setting the template JSON, etc).

First create a certificate-key pair:
``` sh
openssl genrsa -out /tmp/deviceCert.key 2048
```

Next create a certificate signing request from it:
``` sh
openssl req -new -key /tmp/deviceCert.key -out /tmp/deviceCert.csr
```

Finally, you pass the certificate signing request while invoking the Fleet Provisioning sample.

``` sh
python3 samples/service_clients/fleet_provisioning_csr.py --endpoint <endpoint> --cert <file> --key <file> --csr_file <file> --template_name <template name> --template_parameters '{"SerialNumber":"1","DeviceLocation":"Seattle"}'
```

## ⚠️ Usage disclaimer

These code examples interact with services that may incur charges to your AWS account. For more information, see [AWS Pricing](https://aws.amazon.com/pricing/).

Additionally, example code might theoretically modify or delete existing AWS resources. As a matter of due diligence, do the following:

- Be aware of the resources that these examples create or delete.
- Be aware of the costs that might be charged to your account as a result.
- Back up your important data.
