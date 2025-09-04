# Sample apps for the AWS IoT Device SDK v2 for Python
## MQTT5 Samples
#### MQTT5 is the recommended MQTT Client. Additional infomration and usage instructions can be found in the [MQTT5 User Guide](../documents/MQTT5_Userguide.md)
* [X509-based mutual TLS](./mqtt/mqtt5_x509.md)
* [PKCS11](./mqtt/mqtt5_pkcs11_connect.md)
* [Websockets with Sigv4 authentication](./mqtt/mqtt5_aws_websocket.md)
* [AWS Custom Authorizer Lambda Function](./mqtt/mqtt5_custom_auth.md)

## Service Clients
* [Basic Fleet Provisioning](./fleet_provisioning_basic.md)
* [CSR Fleet Provisioning](./fleet_provisioning_csr.md)
* [Shadow](./shadow.md)
* [Jobs](./jobs.md)

## Greengrass
* [Greengrass Discovery](./basic_discovery.md)
* [Greengrass IPC](./ipc_greengrass.md)

### Build instructions

First, install the `aws-iot-devices-sdk-python-v2` with following the instructions from [Installation](../README.md#Installation).

Each sample README has instructions on how to run each sample with the same name as the sample itself. For example, the [MQTT5 PubSub README](./mqtt5_pubsub.md) is `mqtt5_pubsub.md` and it can be run with the following:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pubsub.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key>
```

### Sample Help

All samples will show their options by passing in `--help`. For example:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pubsub.py --help
```

Which will result in output showing all of the options that can be passed in at the command line, along with descriptions of what each does and whether they are optional or not.

### Enable logging in samples

To enable logging in the samples, you need to pass the `--verbosity` as an additional argument. `--verbosity` controls the level of logging shown. `--verbosity` can be set to `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`, or `None`.

For example, to run [MQTT5 PubSub](./mqtt5_pubsub.md) sample with logging you could use the following:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pubsub.py <other arguments> --verbosity Debug
```
