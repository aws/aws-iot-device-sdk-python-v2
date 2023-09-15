# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, http, io
import threading
from concurrent.futures import Future
import time
import json
from utils.command_line_utils import CommandLineUtils

TIMEOUT = 100
topic_filter = "test/topic"

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_mqtt5_pubsub()

io.init_logging(io.LogLevel.Debug, "pubsub.log")

# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure")
    print("Connection failed with exception:{}".format(lifecycle_connection_failure.exception))


if __name__ == '__main__':
    global future_stopped, future_connection_success
    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)


    count = 0
    while True:
        future_stopped = Future()
        future_connection_success = Future()
        count += 1
        print("Start the " + str(count) + " run")
        # Create MQTT5 client
        client = mqtt5_client_builder.mtls_from_path(
            endpoint=cmdData.input_endpoint,
            port=cmdData.input_port,
            cert_filepath=cmdData.input_cert,
            pri_key_filepath=cmdData.input_key,
            ca_filepath=cmdData.input_ca,
            http_proxy_options=proxy_options,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_connection_failure=on_lifecycle_connection_failure,
            client_id=cmdData.input_clientId)
        print("MQTT5 Client Created")

        client.start()
        lifecycle_connect_success_data = future_connection_success.result(TIMEOUT)

        print("Stopping Client")
        client.stop()

        future_stopped.result(TIMEOUT)
        print("Client Stopped!")

