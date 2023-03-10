# WindowsCert Connect

[**Return to main sample list**](./README.md)

This sample is similar to the [Basic Connect](../basic_connect.md) sample, in that it connects via Mutual TLS (mTLS) using a certificate and key file.  However, unlike the Basic Connect where the certificate and private key file are stored on disk, this sample uses a PKCS#12 file stored in the [Windows certificate store](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores). This adds a layer of security because the private key file is not just sitting on the computer and instead is hidden securely away in the [Windows certificate store](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores).

**WARNING: Windows only**

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

To run the Windows certificate connect sample from the `samples` folder, use the following command:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 windows_cert_connect.py --endpoint <endpoint> --cert <path to certificate>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

```sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 windows_cert_connect.py --endpoint <endpoint> --cert <path to certificate> --ca_file <path to root CA>
```

### How to setup and run

To run this sample, you will need the path to your certificate in the [Windows certificate store](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores). This will look something like the following:

```
CurrentUser\MY\A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6
```

Where "CurrentUser\MY" is the store and "A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6" is the certificate's thumbprint. Note that if your certificate and private key are in a [TPM](https://docs.microsoft.com/en-us/windows/security/information-protection/tpm/trusted-platform-module-overview) then you would use them by passing their certificate store path.

The steps to take a AWS IoT Thing certificate and key with the Windows Certificate Connect sample are listed below:

1. Create an IoT Thing with a certificate and key if you haven't already.

2. Combine the certificate and private key into a single `.pfx` file. You will be **prompted for a password while creating this file and it is important that you remember it** for this process. Otherwise you will need to restart and create a new `.pfx` file should you forget the password.

    If you have OpenSSL installed you can run the following to create a `.pfx` file:
    ```powershell
    openssl pkcs12 -in certificate.pem.crt -inkey private.pem.key -out certificate.pfx
    ```

    Otherwise use [CertUtil](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/certutil) to create the `.pfx` file:
    ```powershell
    certutil -mergePFX certificate.pem.crt,private.pem.key certificate.pfx
    ```

3. Add the .pfx file to a Windows certificate store using PowerShell's [Import-PfxCertificate](https://docs.microsoft.com/en-us/powershell/module/pki/import-pfxcertificate)

    ```powershell
    $mypwd = Get-Credential -UserName 'Enter password below' -Message 'Enter password below'
    Import-PfxCertificate -FilePath certificate.pfx -CertStoreLocation Cert:\CurrentUser\My -Password $mypwd.Password
    ```

    Replace `$mypwd.Password` with the password of your `.pfx` file.

    Once you run the command, note the certificate thumbprint that is printed out:

    ```powershell
    Thumbprint                                Subject
    ----------                                -------
    A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6  CN=AWS IoT Certificate
    ```

    In the example above, the certificate's path would be: `CurrentUser\MY\A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6`. This is important as you need to pass this path into the `--cert` argument when running this sample.

4. You can run the sample using the following:

    ```sh
    # For Windows: replace 'python3' with 'python' and '/' with '\'
    python3 windows_cert_connect.py --endpoint <endpoint> --cert <path to certificate>
    ```
