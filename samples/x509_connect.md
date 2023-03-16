# x509 Credentials Provider Connect

[**Return to main sample list**](./README.md)

This sample is similar to the [Basic Connect](./basic_connect.md), but the connection uses a X.509 certificate
to source the AWS credentials when connecting.

See the [Authorizing direct calls to AWS services using AWS IoT Core credential provider](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html) page for instructions on how to setup the IAM roles, the trust policy for the IAM roles, how to setup the IoT Core Role alias, and how to get the credential provider endpoint for your AWS account.

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
    },
    {
      "Effect":"Allow",
      "Action":"iot:AssumeRoleWithCertificate",
      "Resource":"arn:aws:iot:<b>region</b>:<b>account</b>:rolealias/<b>role-alias</b>"
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.
* `<role-alias>`: The X509 role alias you created and wish to connect using.

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

To run the x509 Credentials Provider Connect sample use the following command:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 x509_connect.py --endpoint <endpoint> --signing_region <region> --x509_cert <path to x509 cert> --x509_endpoint <x509 credentials endpoint> --x509_key <path to x509 key> --x509_role_alias <alias> -x509_thing_name <thing name>
```

You can also pass a Certificate Authority file (CA) if your X509 certificate and key combination requires it:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 x509_connect.py --endpoint <endpoint> --signing_region <region> --x509_cert <path to x509 cert> --x509_endpoint <x509 credentials endpoint> --x509_key <path to x509 key> --x509_role_alias <alias> -x509_thing_name <thing name> --x509_ca_file <path to x509 CA file>
```
