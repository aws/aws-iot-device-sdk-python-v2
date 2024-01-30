# Sample apps for the AWS IoT Device SDK v2 for Python
## MQTT5 Samples
#### MQTT5 is the recommended MQTT Client. It has many benefits over MQTT311 outlined in the [MQTT5 User Guide](../documents/MQTT5_Userguide.md)
* [MQTT5 PubSub](./mqtt5_pubsub.md)
    + [Direct MQTT with X509-based mutual TLS](./mqtt5_pubsub.md#direct-mqtt-with-x509-based-mutual-tls)
    + [Direct MQTT with PKCS12 Method](./mqtt5_pubsub.md#direct-mqtt-with-pkcs12-method)
    + [MQTT over Websockets with Sigv4 authentication](./mqtt5_pubsub.md#mqtt-over-websockets-with-sigv4-authentication)
    + [MQTT over Websockets with Cognito authentication](./mqtt5_pubsub.md#mqtt-over-websockets-with-cognito-authentication)
* [MQTT5 Shared Subscription](./mqtt5_shared_subscription.md)
* [MQTT5 PKCS#11 Connect](./mqtt5_pkcs11_connect.md)
* [MQTT5 Custom Authorizer Connect](./mqtt5_custom_authorizer_connect.md)
* [MQTT5 Shadow](./shadow_mqtt5.md)
* [MQTT5 Jobs](./jobs_mqtt5.md)
* [MQTT5 Fleet Provisioning](./fleetprovisioning_mqtt5.md)
## MQTT311 Samples
* [PubSub](./pubsub.md)
* [Basic Connect](./basic_connect.md)
* [Websocket Connect](./websocket_connect.md)
* [PKCS#11 Connect](./pkcs11_connect.md)
* [PKCS#12 Connect](./pkcs12_connect.md)
* [Windows Certificate Connect](./windows_cert_connect/README.md)
* [Custom Authorizer Connect](./custom_authorizer_connect.md)
* [Cognito Connect](./cognito_connect.md)
* [X509 Connect](./x509_connect.md)
* [Shadow](./shadow.md)
* [Jobs](./jobs.md)
* [Fleet Provisioning](./fleetprovisioning.md)
## Other
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
