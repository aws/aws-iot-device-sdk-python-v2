# Sample Applications for the AWS IoT Device SDK v2 for Python
This directory contains sample applications for [aws-iot-device-sdk-python-v2](../README.md).

### Table of Contents
* [Samples](#samples)
    * [MQTT5 Client Samples](#mqtt5-client-samples)
    * [Service Client Samples](#service-client-samples)
    * [Greengrass Samples](#greengrass-samples)
* [Instructions](#instructions)
* [Sample Help](#sample-help)
* [Enable Logging](#enable-logging)


## Samples
### MQTT5 Client Samples
##### MQTT5 is the recommended MQTT Client. Additional infomration and usage instructions can be found in the [MQTT5 User Guide](../documents/MQTT5_Userguide.md). The samples below will create an MQTT5 client, connect using the selected method, subscribe to a topic, publish to the topic, and then disconnect.
| MQTT5 Client Sample | Description |
|--------|-------------|
| [X509-based mutual TLS](./mqtt/mqtt5_x509.md) | Demonstrates connecting to AWS IoT Core using X.509 certificates and private keys.
| [Websockets with Sigv4 authentication](./mqtt/mqtt5_aws_websocket.md) | Shows how to authenticate over websockets using AWS Signature Version 4 credentials. |
| [AWS Custom Authorizer Lambda Function](./mqtt/mqtt5_custom_auth.md) | Examples of connecting with a signed and unsigned Lambda-backed custom authorizer.
| [PKCS11](./mqtt/mqtt5_pkcs11_connect.md) | Demonstrates connecting using a hardware security module (HSM) or smartcard with PKCS#11. |
| [Other Connection Methods](../documents/MQTT5_Userguide.md#how-to-create-an-mqtt5-client-based-on-desired-connection-method) | More connection methods are available for review in the MQTT5 Userguide

### Service Client Samples
##### AWS offers a number of IoT related services using MQTT. The samples below demonstrate how to use the service clients provided by the SDK to interact with those services.
| Service Client Sample | Description |
|--------|-------------|
| [Shadow](./service_clients//shadow.md) | Manage and sync device state using the IoT Device Shadow service. |
| [Jobs](./service_clients//jobs.md) | Receive and execute remote operations sent from the Jobs service. |
| [Basic Fleet Provisioning](./service_clients//fleet_provisioning_basic.md) | Provision a device using the Fleet Provisioning template. |
| [CSR Fleet Provisioning](./service_clients//fleet_provisioning_csr.md) | Demonstrates CSR-based device certificate provisioning. |


### Greengrass Samples
##### Samples that interact with [AWS Greengrass](https://aws.amazon.com/greengrass/).
| Greengrass Sample | Description |
|--------|-------------|
| [Greengrass Discovery](./greengrass//basic_discovery.md) | Discover and connect to a local Greengrass core. |
| [Greengrass IPC](./greengrass//ipc_greengrass.md) | Demonstrates Inter-Process Communication (IPC) with Greengrass components. |

### Instructions

First, install `aws-iot-device-sdk-python-v2`. Installation instructions for the SDK are [Provided Here](../README.md#Installation).

Each sample's README contains prerequisites, arguments, and detailed instructions. For example, the [MQTT5 X509 Sample README](./mqtt/mqtt5_x509.md) is `mqtt5_x509.md` and the sample can be run with the following command:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_x509.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key>
```

### Sample Help

All samples will show their options and arguments by passing in `--help`. For example:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_x509.py --help
```

will result in the following print output:
```
MQTT5 X509 Sample (mTLS)

options:
  -h, --help    show this help message and exit

required arguments:
  --endpoint    IoT endpoint hostname (default: None)
  --cert        Path to the certificate file to use during mTLS connection establishment (default: None)
  --key         Path to the private key file to use during mTLS connection establishment (default: None)

optional arguments:
  --client_id   Client ID (default: mqtt5-sample-5873a450)
  --topic       Topic (default: test/topic)
  --message     Message payload (default: Hello from mqtt5 sample)
  --count       Messages to publish (0 = infinite) (default: 5)
```

The sample will not run without the required arguments and will notify you of missing arguments.

### Enable Logging

Instructions to enable logging are available in the [FAQ](../documents/FAQ.md) under [How do I enable logging](../documents/FAQ.md#how-do-i-enable-logging).

## ⚠️ Usage disclaimer

These code examples interact with services that may incur charges to your AWS account. For more information, see [AWS Pricing](https://aws.amazon.com/pricing/).

Additionally, example code might theoretically modify or delete existing AWS resources. As a matter of due diligence, do the following:

- Be aware of the resources that these examples create or delete.
- Be aware of the costs that might be charged to your account as a result.
- Back up your important data.
