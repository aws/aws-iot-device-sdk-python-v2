# Jobs MQTT5

[**Return to main sample list**](./README.md)

This sample uses the AWS IoT [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) Service to describe jobs to execute. [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) is a service that allows you to define and respond to remote operation requests defined through the AWS IoT Core website or via any other device (or CLI command) that can access the [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) service.

Note: This sample requires you to create jobs for your device to execute. See
[instructions here](https://docs.aws.amazon.com/iot/latest/developerguide/create-manage-jobs.html) for how to make jobs.

On startup, the sample describes the jobs that are pending execution and pretends to process them, marking each job as complete as it does so.

Your IoT Core Thing's [Policy](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html) must provide privileges for this sample to connect, subscribe, publish, and receive. Below is a sample policy that can be used on your IoT Core Thing that will allow this sample to run as intended.

<details>
<summary>Sample Policy</summary>
<pre>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/start-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/update",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/get",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/get"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Receive",
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/notify-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/start-next/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/update/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/get/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topic/$aws/things/<b>thingname</b>/jobs/*/get/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": [
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/notify-next",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/start-next/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/*/update/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/get/*",
        "arn:aws:iot:<b>region</b>:<b>account</b>:topicfilter/$aws/things/<b>thingname</b>/jobs/*/get/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:<b>region</b>:<b>account</b>:client/test-*"
    }
  ]
}
</pre>

Replace with the following with the data from your AWS account:
* `<region>`: The AWS IoT Core region where you created your AWS IoT Core thing you wish to use with this sample. For example `us-east-1`.
* `<account>`: Your AWS IoT Core account ID. This is the set of numbers in the top right next to your AWS account name when using the AWS IoT Core website.
* `<thingname>`: The name of your AWS IoT Core thing you want the device connection to be associated with

Note that in a real application, you may want to avoid the use of wildcards in your ClientID or use them selectively. Please follow best practices when working with AWS on production applications using the SDK. Also, for the purposes of this sample, please make sure your policy allows a client ID of `test-*` to connect or use `--client_id <client ID here>` to send the client ID your policy supports.

</details>

## How to run

Use the following command to run the Jobs sample from the `samples` folder:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 jobs_mqtt5.py --endpoint <endpoint> --cert <file> --key <file> --thing_name <name>
```

You can also pass a Certificate Authority file (CA) if your certificate and key combination requires it:

``` sh
# For Windows: replace 'python3' with 'python' and '/' with '\'
python3 jobs_mqtt5.py --endpoint <endpoint> --cert <file> --key <file> --thing_name <name> --ca_file <file>
```


## Service Client Notes
### Difference relative to MQTT311 IotJobsClient
The IotJobsClient with mqtt5 client is almost identical to the mqtt3 one. The only difference is that you would need setup up a Mqtt5 Client and pass it to the IotJobsClient.
For how to setup a Mqtt5 Client, please refer to [MQTT5 UserGuide](../documents/MQTT5_Userguide.md) and [MQTT5 PubSub Sample](./mqtt5_pubsub.py)

<table>
<tr>
<th>Create a IotJobsClient with Mqtt5</th>
<th>Create a IotJobsClient with Mqtt311</th>
</tr>
<tr>
<td>

```python
  # Create a Mqtt5 Client
  mqtt5_client = mqtt5_client_builder.mtls_from_path(
          endpoint,
          port,
          cert_filepath,
          pri_key_filepath,
          ca_filepath,
          client_id,
          clean_session,
          keep_alive_secs,
          http_proxy_options,
          on_lifecycle_connection_success,
          on_lifecycle_stopped)

  # Create the Jobs client from Mqtt5 Client
  jobs_client = iotjobs.IotJobsClient(mqtt5_client)
```

</td>
<td>

```python
    # Create a Mqtt311 Connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint,
        port,
        cert_filepath,
        pri_key_filepath,
        ca_filepath,
        client_id,
        clean_session,
        keep_alive_secs,
        http_proxy_options)

    # Create the Jobs client from Mqtt311 Connection
    jobs_client = iotjobs.IotJobsClient(mqtt_connection)
```

</td>
</tr>
</table>

### Mqtt5.QoS v.s. Mqtt3.QoS
As the service client interface is unchanged for both Mqtt3 Connection and Mqtt5 Client,the IotJobsClient will use Mqtt3.QoS instead of Mqtt5.QoS even with a Mqtt5 Client. You could use mqtt3.QoS.to_mqtt5() and mqtt5.QoS.to_mqtt3() to convert the value.