# Websocket Connect with static credentials

[**Return to main sample list**](../../README.md)

This sample makes an MQTT connection via Websockets and then disconnects.
On startup, the device connects to the server via Websockets then disconnects right after.
This sample demonstrates connecting via static credentials.

If you want to use simple or custom auth (or static creds, or basic auth, etc) instead,
then you will need to replace part of the sample (connection\_setup function) with a code snippet we provided in its corresponding readme.

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

<details>
<summary>(see sample policy)</summary>
<pre language=json>
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

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

For this sample, using Websockets will attempt to fetch the AWS credentials to authorize the connection from static credentials.

</details>


<details>
<summary> (code snipet to replace similar section)</summary>
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

