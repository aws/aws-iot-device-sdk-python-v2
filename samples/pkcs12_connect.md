# PKCS12 Connect

[**Return to main sample list**](../README.md)

This sample is similar to the [Basic Connect](../BasicConnect/README.md) sample, in that it connects via Mutual TLS (mTLS) using a certificate and key file.  However, unlike the Basic Connect where the certificate and private key file are stored on disk, this sample uses a PKCS#12 file instead.

**WARNING: MacOS only**. Currently, TLS integration with PKCS12 is only available on MacOS devices.

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

To run the PKCS12 connect use the following command:

```sh
python3 pkcs12_connect --endpoint <endpoint> --pkcs12_file <path to PKCS12 file> --pkcs12_password <password for PKCS12 file>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
python3 pkcs12_connect --endpoint <endpoint> --pkcs12_file <path to PKCS12 file> --pkcs12_password <password for PKCS12 file> --ca_file <path to CA file>
```

### How to setup and run

To use the certificate and key files provided by AWS IoT Core, you will need to convert them into PKCS#12 format and then import them into your Java keystore. You can convert the certificate and key file to PKCS12 using the following command:

```sh
openssl pkcs12 -export -in <my-certificate.pem.crt> -inkey <my-private-key.pem.key> -out <my-pkcs12-key.pem.key> -name <alias here> -password pass:<password here>
```

Once converted, you can then run the PKCS12 connect sample with the following:

```sh
python3 pkcs12_connect --endpoint <endpoint> --pkcs12_file <my-pkcs12-key.pem.key> --pkcs12_password <password here>
```
