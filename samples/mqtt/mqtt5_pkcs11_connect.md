# MQTT5 PKCS#11 PubSub

[**Return to main sample list**](../README.md)
*__Jump To:__*
* [Introduction](#introduction)
* [Requirements](#requirements)
* [How To Run](#how-to-run)
* [Run Sample with Soft HSM](#run-sample-with-softhsm)
* [Additional Information](#additional-information)

## Introduction
This sample is similar to the [MQTT5 X509](./mqtt5_x509.md) sample in that it connects via Mutual TLS (mTLS) using a certificate and key file. However, unlike the x509 sample where the certificate and private key file are stored on disk, this sample uses a PKCS#11 compatible smart card or Hardware Security Module (HSM) to store and access the private key file. This adds a layer of security because the private key file is not openly on the computer but instead is hidden securely away behind the PKCS#11 device.

You can read more about MQTT5 for the Python IoT Device SDK V2 in the [MQTT5 user guide](../../documents/MQTT5_Userguide.md).

## Requirements

**WARNING: Unix (Linux) only**. Currently, TLS integration with PKCS#11 is only available on Unix devices.

This sample assumes you have the required AWS IoT resources available. Information about AWS IoT can be found [HERE](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) and instructions on creating AWS IoT resources (AWS IoT Policy, Device Certificate, Private Key) can be found [HERE](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html).

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:client/mqtt5-sample-*"
      ]
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `mqtt5-sample-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

The MQTT5 PKCS11 connect sample can be run from the `samples\mqtt` folder using the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pkcs11_connect.py \
  --endpoint <AWS IoT endpoint> \
  --cert <path to certificate file> \
  --pkcs11_lib <Path to PKCS#11 Library> \
  --pin <User PIN for logging into PKCS#11 token> \
  --token_label <Label of the PKCS#11 token to use (optional)> \
  --key_label <Label of private key on the PKCS#11 token (optional)>
```

If you would like to see what optional arguments are available, use the `--help` argument:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pkcs11_connect.py --help
```
will result in the following output:
```
MQTT5 PKCS11 Sample.

options:
  -h, --help      show this help message and exit

required arguments:
  --endpoint      IoT endpoint hostname (default: None)
  --cert          Path to the certificate file to use during mTLS connection establishment (default: None)
  --pkcs11_lib    Path to PKCS#11 Library (default: None)
  --pin           User PIN for logging into PKCS#11 token (default: None)

optional arguments:
  --token_label   Label of the PKCS#11 token to use (optional). (default: None)
  --slot_id       Slot ID containing the PKCS#11 token to use (optional). (default: None)
  --key_label     Label of private key on the PKCS#11 token (optional). (default: None)
  --topic         Topic (default: test/topic)
  --message       Message payload (default: Hello from mqtt5 sample)
  --count         Messages to publish (0 = infinite) (default: 5)
  --client_id     Client ID (default: mqtt5-sample-<uuid>)
  ```

### Run sample with SoftHSM

If you do not have a PKCS#11 device and/or want to use a software-based solution for testing, you can use [SoftHSM2](https://www.opendnssec.org/softhsm/) as the PKCS#11 device. This allows testing without the need to purchase and use separate hardware.

The steps to use [SoftHSM2](https://www.opendnssec.org/softhsm/) as the PKCS#11 device with this sample are listed below:

1. Create an AWS IoT Thing with a certificate and key if you haven't already.

2. Convert the private key from the AWS IoT Thing into PKCS#8 format using the following command:

    ```sh
    openssl pkcs8 -topk8 -in <private.pem.key> -out <private.p8.key> -nocrypt
    ```

3. Install [SoftHSM2](https://www.opendnssec.org/softhsm/) using `apt`:

    ```sh
    sudo apt install softhsm
    ```

    Note that if you are using a Linux distribution that does not include `apt`, you will need to
    adjust the above command to get [SoftHSM2](https://www.opendnssec.org/softhsm/) from the package manager your distribution supports.

4. Check that [SoftHSM2](https://www.opendnssec.org/softhsm/) is working as expected by running the following:

    ```sh
    softhsm2-util --show-slots
    ```

    If this spits out an error message, create a config file:
    *   Default location: `~/.config/softhsm2/softhsm2.conf`
    *   This file must specify token dir, default value is:
        ```sh
        directories.tokendir = /usr/local/var/lib/softhsm/tokens/
        ```

5. Create a token and import the private key you converted in step 2:

    You can use any values for the labels, PINs, etc

    ```sh
    softhsm2-util --init-token --free --label <token-label> --pin <user-pin> --so-pin <so-pin>
    ```

    **Important**: Note which slot the token ended up in

    ```sh
    softhsm2-util --import <private.p8.key> --slot <slot-with-token> --label <key-label> --id <hex-chars> --pin <user-pin>
    ```

6. Now you can run the sample with the following:

    ```sh
    # For Windows: replace 'python3' with 'python' and '/' with '\'
    python3 mqtt5_pkcs11_connect.py --endpoint <endpoint> --cert <path to certificate> --pkcs11_lib <path to PKCS11 lib> --pin <user-pin> --token_label <token-label> --key_label <key-label>
    ```
  
  ## Additional Information
Additional help with the MQTT5 Client can be found in the [MQTT5 Userguide](../../documents/MQTT5_Userguide.md). This guide will provide more details on MQTT5 [operations](../../documents/MQTT5_Userguide.md#optional-keyword-arguments), [lifecycle events](../../documents/MQTT5_Userguide.md#lifecycle-events), [connection methods](../../documents/MQTT5_Userguide.md#connecting-to-aws-iot-core), and other useful information.

## ⚠️ Usage disclaimer

These code examples interact with services that may incur charges to your AWS account. For more information, see [AWS Pricing](https://aws.amazon.com/pricing/).

Additionally, example code might theoretically modify or delete existing AWS resources. As a matter of due diligence, do the following:

- Be aware of the resources that these examples create or delete.
- Be aware of the costs that might be charged to your account as a result.
- Back up your important data.
