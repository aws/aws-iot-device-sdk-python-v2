# Custom Authorizer Connect

[**Return to main sample list**](./README.md)

This sample makes an MQTT5 connection and connects through a [Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html). On startup, the device connects to the server and then disconnects. This sample is for reference on connecting using a Custom Authorizer with MQTT5. Using a Custom Authorizer allows you to perform your own authorization using an AWS Lambda function. See [Custom Authorizer](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html) for more information.

You will need to setup your Custom Authorizer so that the lambda function returns a policy document. See [this page on the documentation](https://docs.aws.amazon.com/iot/latest/developerguide/config-custom-auth.html) for more details and example return result. You can customize this lambda function as needed for your application to provide your own security measures based on the needs of your application.

MQTT5 introduces additional features and enhancements that improve the development experience with MQTT. You can read more about MQTT5 in the Python V2 SDK by checking out the [MQTT5 user guide](../documents/MQTT5_Userguide.md).

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

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

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

# How to run

**Note** The sample also allows passing arguments to specify additional data your custom authorizer may need. The snippets below assume that the custom authorizer does not need these additional parameters, but in the general case, you will almost always need some of them depending on the authorizer's configuration and the associated Lambda function's internals.
* `--custom_auth_username` - opaque string value passed to the authorizer via an MQTT Connect packet.  The authorizer's Lambda can check this value from the event JSON value it receives as input: `event.protocolData.mqtt.username`
* `--custom_auth_password` - opaque binary value passed to the authorizer via an MQTT Connect packet.  The authorizer's Lambda can check this value from the event JSON value it receives as input: `event.protocolData.mqtt.password`
* `--custom_auth_token_key_name` - (Signed authorizers only) The query string parameter name that the token value should be bound to in the MQTT Connect packet.
* `--custom_auth_token_value` - (Signed authorizers only) An arbitrary value chosen by the user.  The user must also submit a digital signature of this value using the private key associated with the authorizer.
* `--custom_auth_authorizer_signature` - (Signed authorizers only) a digital signature of the value of the `--custom_auth_token_value` parameter using the private key associated with the authorizer.  The binary signature value must be base64 encoded and then URI encoded; the SDK will not do this for you.

## MQTT over TCP with TLS

To run the MQTT5 Custom Authorizer connect sample from the `samples` folder using TCP, use the following command:

``` sh
# For Windows: replace 'python3' with 'python'
python3 mqtt5_custom_authorizer_connect.py --endpoint <endpoint> --custom_auth_authorizer_name <authorizer name>
```

## MQTT over Websockets with TLS

To run the MQTT5 Custom Authorizer connect sample from the `samples` folder using Websockets, use the following command:

``` sh
# For Windows: replace 'python3' with 'python'
python3 mqtt5_custom_authorizer_connect.py --endpoint <endpoint> --use_websockets "true" --custom_auth_authorizer_name <authorizer name>
```
