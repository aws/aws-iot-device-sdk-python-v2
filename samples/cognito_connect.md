# Cognito Connect

[**Return to main sample list**](./README.md)

This sample is similar to the [Websocket Connect sample](./websocket_connect.md), but instead of sourcing the AWS credentials from the environment files or local files, it instead uses a [Cognito](https://aws.amazon.com/cognito/) identity to authorize the connection. This has the advantage of not requiring the needing to store AWS credentials on the device itself with permissions to perform the IoT actions your device requires, but instead just having AWS credentials for the [Cognito](https://aws.amazon.com/cognito/) identity instead. This provides a layer of security and indirection that gives you better security.

On startup, the device connects to the server and then disconnects. This sample is for reference on connecting using Cognito.

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

## How to run

To run this sample, you need to have a Cognito identifier ID. You can get a Cognito identifier ID by creating a Cognito identity pool. For creating Cognito identity pools, please see the following page on the AWS documentation: [Tutorial: Creating an identity pool](https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-identity-pool.html)
You should also add _iot:Connect_ permission to the role added to congnito  or the default role created automatically when creating the new identity (or create a
<details>
<summary> (see sample policy)</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cognito-identity:GetCredentialsForIdentity",
        "iot:Connect"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
</pre>
</details>

**Note:** This sample assumes using an identity pool with unauthenticated identity access for the sake of convenience. Please follow best practices in a real world application based on the needs of your application and the intended use case.

Once you have a Cognito identity pool, you can run the following CLI command to get the Cognito identity pool ID:
```sh
aws cognito-identity get-id --identity-pool-id <cognito identity pool id>
# result from above command
{
    "IdentityId": "<cognito identity ID>"
}
```

You can then use the returned ID in the `IdentityId` result as the input for the `--cognito_identity` argument. Please note that the Cognito identity pool ID is **not** the same as a Cognito identity ID and the sample will not work if you pass a Cognito pool id.

To run the Cognito connect sample from the `samples` folder, use the following command:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 cognito_connect.py --endpoint <endpoint> --signing_region <signing region> --cognito_identity <cognito identity ID>
```
