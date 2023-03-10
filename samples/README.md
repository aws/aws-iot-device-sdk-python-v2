# Sample apps for the AWS IoT Device SDK v2 for Python

* [MQTT5 PubSub](./mqtt5_pubsub/README.md)
* [PubSub](./pubsub/README.md)
* [Basic Connect](./basic_connect/README.md)
* [Websocket Connect](./websocket_connect/README.md)
* [MQTT5 PKCS#11 Connect](./mqtt5_pkcs11_connect/README.md)
* [PKCS#11 Connect](./pkcs11_connect/README.md)
* [Windows Certificate Connect](./windows_cert_connect/README.md)
* [MQTT5 Custom Authorizer Connect](./mqtt5_custom_authorizer_connect/README.md)
* [Custom Authorizer Connect](./custom_authorizer_connect/README.md)
* [Cognito Connect](./cognito_connect/README.md)
* [Shadow](./shadow/README.md)
* [Jobs](./jobs/README.md)
* [Fleet Provisioning](./identity/README.md)
* [Greengrass Discovery](./discovery_greengrass/README.md)
* [Greengrass IPC](./ipc_greengrass/README.md)

### Build instructions

First, install the `aws-iot-devices-sdk-python-v2` with following the instructions from [Installation](../README.md#Installation).

Then change into the `samples` folder/directory to run the Python commands to execute the samples. Each sample README has instructions on how to run each sample and each sample can be run from the `samples` folder. For example, to run the [PubSub](./pubsub/README.md) sample:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub/pubsub.py --endpoint <endpoint> --cert <path to certificate> --key <path to private key>
```

### Sample Help

All samples will show their options by passing in `--help`. For example:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub/pubsub.py --help
```

Which will result in output showing all of the options that can be passed in at the command line, along with descriptions of what each does and whether they are optional or not.

### Enable logging in samples

To enable logging in the samples, you need to pass the `--verbosity` as an additional argument. `--verbosity` controls the level of logging shown. `--verbosity` can be set to `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`, or `None`.

For example, to run [PubSub](./pubsub/README.md) sample with logging you could use the following:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 pubsub/pubsub.py <other arguments> --verbosity Debug
```
