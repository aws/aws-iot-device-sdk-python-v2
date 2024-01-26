# Websocket Connect

[**Return to main sample list**](./README.md)
If you want to use custom auth (or static creds, or basic auth, etc) instead,
then you will need to replace part of the sample (connection\_setup function) with a code snippet we provided in its corresponding readme.

* [Websocket Connection Using Custom Authentication](#websocket-connection-using-custom-authentication)
* [Websocket Connection Using Static Credentials](#websocket-connection-using-custom-authentication)

This sample makes an MQTT connection via Websockets and then disconnects.
On startup, the device connects to the server via Websockets and then disconnects right after.
This sample is for reference on connecting via Websockets.
This sample demonstrates the most straightforward way to connect via Websockets by querying the AWS credentials for the connection from the device's environment variables or local files.

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect.
Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

<details>
<summary>(see sample policy)</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
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

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively.
Please follow best practices when working with AWS on production applications using the SDK.
Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

For this sample, using Websockets will attempt to fetch the AWS credentials to authorize the connection from your environment variables or local files.
See the [authorizing direct AWS](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html) page for documentation on how to get the AWS credentials, which then you can set to the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables.

</details>

## How to run

Optional parameters:
```
--proxy_host <str>
--proxy_port <int>
```
To run the websocket connect from the `samples` folder, use the following command:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 websocket_connect.py --endpoint <endpoint> --signing_region <signing region> --proxy_host <str> --proxy_port <int>
```


# Websocket Connection Using Custom Authentication

This sample makes an MQTT connection and connects through a [Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html).
On startup, the device connects to the server and then disconnects.
This sample is for reference on connecting using a Custom Authorizer.
Using a Custom Authorizer allows you to perform your own authorization using an AWS Lambda function.
See [Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html) for more information.
You will need to setup your Custom Authorizer so that the lambda function returns a policy document.
See [this page on the documentation](https://docs.aws.amazon.com/iot/latest/developerguide/config-custom-auth.html) for more details and example return result.
You can customize this lambda function as needed for your application to provide your own security measures based on the needs of your application.
Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect.
Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

If you want to use simple or custom auth (or static creds, or basic auth, etc) instead,
then you will need to replace part of the sample (connection\_setup function) with a code snippet we provided in its corresponding readme.

<details>
<summary> (code snipet to replace the similar function)</summary>
<pre language="python">
<code>
def connection_setup():
    # cmdData is the arguments/input from the command line placed into a single struct for
    # use in this sample. This handles all of the command line parsing, validating, etc.
    # See the Utils/CommandLineUtils for more information.
    cmdData = CommandLineUtils.parse_sample_input_custom_authorizer_connect()
    # Create the proxy options if the data is present in cmdData
    proxy_options = None

    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    # Create a default credentials provider and a MQTT connection from the command line data
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain()

    mqtt_connection = mqtt_connection_builder.websockets_with_custom_authorizer(
        endpoint=cmdData.input_endpoint,
        credentials_provider=credentials_provider,
        auth_username=cmdData.input_input_custom_auth_username,
        auth_authorizer_name=cmdData.input_custom_authorizer_name,
        auth_authorizer_signature=cmdData.input_custom_authorizer_signature,
        auth_password=cmdData.input_custom_auth_password,
        auth_token_key_name=cmdData.input_custom_authorizer_token_key_name,
        auth_token_value=cmdData.input_custom_authorizer_token_value,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30)

    return mqtt_connection, cmdData

</code>
</pre>
</details>

## How to run
Options for custom auth
```
--custom_auth_username <str>
--custom_auth_authorizer_name <str>
--custom_auth_authorizer_signature <str>
--custom_auth_password <str>
--custom_auth_token_name <str>
--custom_auth_token_value <str>
```

To run the websocket connect from the `samples` folder, use the following command:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 websocket_connect.py --endpoint <endpoint> --custom_auth_username <str> --custom_auth_authorizer_name <str> --custom_auth_authorizer_signature <str> --custom_auth_password <str> --custom_auth_token_name <str> --custom_auth_token_value <str>
```


# Websocket Connection Using Static Credentials
This sample makes an MQTT connection via Websockets and then disconnects.
On startup, the device connects to the server via Websockets then disconnects right after.
This sample demonstrates connecting via static credentials.

If you want to use simple or custom auth (or static creds, or basic auth, etc) instead,
then you will need to replace part of the sample (connection\_setup function) with a code snippet we provided in its corresponding readme.

For this sample, using Websockets will attempt to fetch the AWS credentials to authorize the connection from static credentials.

<details>
<summary> (code snipet to replace the similar function)</summary>
<pre language=cpp>
<code >
def connection_setup():
    # cmdData is the arguments/input from the command line placed into a single struct for
    # use in this sample. This handles all of the command line parsing, validating, etc.
    # See the Utils/CommandLineUtils for more information.
    cmdData = CommandLineUtils.parse_sample_input_static_credentials_connect()

    cred_provider = AwsCredentialsProvider.new_static(
        access_key_id=cmdData.input_access_key_id,
        secret_access_key=cmdData.input_secret_access_key,
        session_token=cmdData.input_session_token)

    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        region=cmdData.input_signing_region,
        credentials_provider=cred_provider,
        endpoint=cmdData.input_endpoint,
        client_id=cmdData.input_clientId)

    return mqtt_connection, cmdData
</code>
</pre>
</details>

## How to run

Options for static credentials
```
--access_key_id <str>
--secret_access_key <str>
--session_token <str>
```

To run the websocket connect from the `samples` folder, use the following command:
``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 websocket_connect.py --endpoint <endpoint> --signing_region <signing region> --access_key_id <str> --secret_access_key <str> --session_token <str>
```

