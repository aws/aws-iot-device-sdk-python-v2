# Basic Connect

[**Return to main sample list**](./README.md)

This sample makes an MQTT connection using a certificate and key file using Mutual TLS (mTLS). On startup, the device connects to the server using the certificate and key files, and then disconnects. This sample is for reference on connecting via certificate and key files. Using a certificate and key file pair is the easiest and most straightforward way to authenticate a connection to AWS IoT Core.

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

To run the basic connect sample from the `samples` folder, use the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 basic_connect.py --endpoint <endpoint> --cert <file> --key <file>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 basic_connect.py --endpoint <endpoint> --cert <file> --key <file> --ca_file <file>
```
