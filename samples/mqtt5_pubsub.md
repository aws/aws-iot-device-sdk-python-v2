# MQTT5 PubSub

[**Return to main sample list**](./README.md)

This sample uses the
[Message Broker](https://docs.aws.amazon.com/iot/latest/developerguide/iot-message-broker.html)
for AWS IoT to send and receive messages through an MQTT connection using MQTT5.

MQTT5 introduces additional features and enhancements that improve the development experience with MQTT. You can read more about MQTT5 in the Python V2 SDK by checking out the [MQTT5 user guide](../documents/MQTT5_Userguide.md).

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
        "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
      ]
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

To Run this sample from the `samples` folder, use the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pubsub.py --endpoint <endpoint> --cert <file> --key <file>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 mqtt5_pubsub.py --endpoint <endpoint> --cert <file> --key <file> --ca_file <file>
```

## **Alternate Connection Configuration Methods supported by AWS IoT Core**
### **Optional Keyword Arguments**
All lifecycle events and the callback for publishes received by the MQTT5 Client should be added to the builder on creation of the Client. A full list of accepted arguments can be found in the API guide.

* [Direct MQTT with X509-based mutual TLS](#direct-mqtt-with-x509-based-mutual-tls)
* [Direct MQTT with Custom Authentication](./mqtt5_custom_authorizer_connect.md)
* [Direct MQTT with PKCS11 Method](./mqtt5_pkcs11_connect.md)
* [Direct MQTT with PKCS12 Method](#direct-mqtt-with-pkcs12-method)
* [MQTT over Websockets with Sigv4 authentication](#mqtt-over-websockets-with-sigv4-authentication)
* [MQTT over Websockets with Cognito authentication](#mqtt-over-websockets-with-cognito-authentication)
* [Direct MQTT with Windows Certificate Store Method](#direct-mqtt-with-windows-certificate-store-method)
### HTTP Proxy
* [Adding an HTTP Proxy](#adding-an-http-proxy)

#### **Direct MQTT with X509-based mutual TLS**
For X509 based mutual TLS, you can create a client where the certificate and private key are configured by path:

```python
    # X.509 based certificate file
    cert_filepath = "<certificate file path>"
    # PKCS#1 or PKCS#8 PEM encoded private key file
    pri_key_filepath = "<private key file path>"

    # other builder configurations can be added using **kwargs in the builder

    # Create an MQTT5 Client using mqtt5_client_builder
    client = mqtt5_client_builder.mtls_from_path(
        endpoint = "<account-specific endpoint>",
        cert_filepath=cert_filepath,
        pri_key_filepath=pri_key_filepath))
```

#### **Direct MQTT with PKCS12 Method**

A MQTT5 direct connection can be made using a PKCS12 file rather than using a PEM encoded private key. To create a MQTT5 builder configured for this connection, see the following code:

```python
    # other builder configurations can be added using **kwargs in the builder

    client = mqtt5_client_builder.mtls_with_pkcs12(
        pkcs12_filepath = "<PKCS12 file path>,
        pkcs12_password = "<PKCS12 password>
        endpoint = "<account-specific endpoint>")
```

**Note**: Currently, TLS integration with PKCS#12 is only available on MacOS devices.

#### **MQTT over Websockets with Sigv4 authentication**
Sigv4-based authentication requires a credentials provider capable of sourcing valid AWS credentials. Sourced credentials
will sign the websocket upgrade request made by the client while connecting.  The default credentials provider chain supported by
the SDK is capable of resolving credentials in a variety of environments according to a chain of priorities:

```Environment -> Profile (local file system) -> STS Web Identity -> IMDS (ec2) or ECS```

If the default credentials provider chain and built-in AWS region extraction logic are sufficient, you do not need to specify
any additional configuration:

```python
    # The signing region. e.x.: 'us-east-1'
    signing_region = "<signing region>"
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain()

    # other builder configurations can be added using **kwargs in the builder

    # Create an MQTT5 Client using mqtt5_client_builder
    client = mqtt5_client_builder.websockets_with_default_aws_signing(
        endpoint = "<account-specific endpoint>",
        region = signing_region,
        credentials_provider=credentials_provider))
```

#### **MQTT over Websockets with Cognito authentication**

A MQTT5 websocket connection can be made using Cognito to authenticate rather than the AWS credentials located on the device or via key and certificate. Instead, Cognito can authenticate the connection using a valid Cognito identity ID. This requires a valid Cognito identity ID, which can be retrieved from a Cognito identity pool. A Cognito identity pool can be created from the AWS console.

To create a MQTT5 builder configured for this connection, see the following code:

```python
    # The signing region. e.x.: 'us-east-1'
    signing_region = "<signing region>"

    # See https://docs.aws.amazon.com/general/latest/gr/cognito_identity.html for Cognito endpoints
    cognito_endpoint = "cognito-identity." + signing_region + ".amazonaws.com"
    cognito_identity_id = "<Cognito identity ID>"
    credentials_provider = auth.AwsCredentialsProvider.new_cognito(
        endpoint=cognito_endpoint,
        identity=cognito_identity_id,
        tls_ctx=io.ClientTlsContext(TlsContextOptions()))

    # other builder configurations can be added using **kwargs in the builder

    # Create an MQTT5 Client using mqtt5_client_builder
    client = mqtt5_client_builder.websockets_with_default_aws_signing(
        endpoint = "<account-specific endpoint>",
        region = signing_region,
        credentials_provider=credentials_provider))
```

**Note**: A Cognito identity ID is different from a Cognito identity pool ID and trying to connect with a Cognito identity pool ID will not work. If you are unable to connect, make sure you are passing a Cognito identity ID rather than a Cognito identity pool ID.

#### **Direct MQTT with Windows Certificate Store Method**
A MQTT5 direct connection can be made with mutual TLS with the certificate and private key in the Windows certificate
store, rather than simply being files on disk. To create a MQTT5 builder configured for this connection, see the
following code:

```python
    client = mqtt5_client_builder.mtls_with_windows_cert_store_path(
        cert_store_path="<CurrentUser\\MY\\A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6>",
        endpoint="<client specific endpoint>")
```

**Note**: Windows Certificate Store connection support is only available on Windows devices.

## **Adding an HTTP Proxy**
No matter what your connection transport or authentication method is, you may connect through an HTTP proxy
by adding the http_proxy_options keyword argument to the builder:

```python
    http_proxy_options = http.HttpProxyOptions(
        host_name = "<proxy host>",
        port = <proxy port>)

    # Create an MQTT5 Client using mqtt5_client_builder with proxy options as keyword argument
    client = mqtt5_client_builder.mtls_from_path(
        endpoint = "<account-specific endpoint>",
        cert_filepath = "<certificate file path>",
        pri_key_filepath = "<private key file path>",
        http_proxy_options = http_proxy_options))
```

SDK Proxy support also includes support for basic authentication and TLS-to-proxy.  SDK proxy support does not include any additional
proxy authentication methods (kerberos, NTLM, etc...) nor does it include non-HTTP proxies (SOCKS5, for example).
