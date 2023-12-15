# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, mqtt5, http
from awsiot import iotjobs, mqtt_connection_builder
from awsiot import iotjobs, mqtt5_client_builder
from concurrent.futures import Future
import sys
import threading
import time
import traceback
import time
from utils.command_line_utils import CommandLineUtils

# - Overview -
# This sample uses the AWS IoT Jobs Service to get a list of pending jobs and
# then execution operations on these pending jobs until there are no more
# remaining on the device. Imagine periodic software updates that must be sent to and
# executed on devices in the wild.
#
# - Instructions -
# This sample requires you to create jobs for your device to execute. See:
# https://docs.aws.amazon.com/iot/latest/developerguide/create-manage-jobs.html
#
# - Detail -
# On startup, the sample tries to get a list of all the in-progress and queued
# jobs and display them in a list. Then it tries to start the next pending job execution.
# If such a job exists, the sample emulates "doing work" by spawning a thread
# that sleeps for several seconds before marking the job as SUCCEEDED. When no
# pending job executions exist, the sample sits in an idle state.
#
# The sample also subscribes to receive "Next Job Execution Changed" events.
# If the sample is idle, this event wakes it to start the job. If the sample is
# already working on a job, it remembers to try for another when it's done.
# This event is sent by the service when the current job completes, so the
# sample will be continually prompted to try another job until none remain.

# Using globals to simplify sample code
is_sample_done = threading.Event()

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
cmdData = CommandLineUtils.parse_sample_input_jobs()

mqtt_connection = None
jobs_client = None
jobs_thing_name = cmdData.input_thing_name
mqtt_qos = None

# MQTT5 specific
mqtt5_client = None
future_connection_success = Future()

class LockedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.disconnect_called = False
        self.is_working_on_job = False
        self.is_next_job_waiting = False
        self.got_job_response = False


locked_data = LockedData()

# Function for gracefully quitting this sample
def exit(msg_or_exception):
    if isinstance(msg_or_exception, Exception):
        print("Exiting Sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    else:
        print("Exiting Sample:", msg_or_exception)

    with locked_data.lock:
        if not locked_data.disconnect_called:
            print("Disconnecting...")
            locked_data.disconnect_called = True
            if cmdData.input_mqtt_version == 5:
                locked_data.disconnect_called = True
                mqtt5_client.stop()
            else:
                future = mqtt_connection.disconnect()
                future.add_done_callback(on_disconnected)


def try_start_next_job():
    print("Trying to start the next job...")
    with locked_data.lock:
        if locked_data.is_working_on_job:
            print("Nevermind, already working on a job.")
            return

        if locked_data.disconnect_called:
            print("Nevermind, sample is disconnecting.")
            return

        locked_data.is_working_on_job = True
        locked_data.is_next_job_waiting = False

    print("Publishing request to start next job...")
    request = iotjobs.StartNextPendingJobExecutionRequest(thing_name=jobs_thing_name)
    publish_future = jobs_client.publish_start_next_pending_job_execution(request, mqtt_qos)
    publish_future.add_done_callback(on_publish_start_next_pending_job_execution)


def done_working_on_job():
    with locked_data.lock:
        locked_data.is_working_on_job = False
        try_again = locked_data.is_next_job_waiting
    exit(0)

    if try_again:
        try_start_next_job()


def on_disconnected(disconnect_future):
    # type: (Future) -> None
    print("Disconnected.")

    # Signal that sample is finished
    is_sample_done.set()


# A list to hold all the pending jobs
available_jobs = []


def on_get_pending_job_executions_accepted(response):
    # type: (iotjobs.GetPendingJobExecutionsResponse) -> None
    with locked_data.lock:
        if (len(response.queued_jobs) > 0 or len(response.in_progress_jobs) > 0):
            print("Pending Jobs:")
            for job in response.in_progress_jobs:
                available_jobs.append(job)
                print(f"  In Progress: {job.job_id} @ {job.last_updated_at}")
            for job in response.queued_jobs:
                available_jobs.append(job)
                print(f"  {job.job_id} @ {job.last_updated_at}")
        else:
            print("No pending or queued jobs found!")
        locked_data.got_job_response = True


def on_get_pending_job_executions_rejected(error):
    # type: (iotjobs.RejectedError) -> None
    print(f"Request rejected: {error.code}: {error.message}")
    exit("Get pending jobs request rejected!")


def on_next_job_execution_changed(event):
    # type: (iotjobs.NextJobExecutionChangedEvent) -> None
    try:
        execution = event.execution
        if execution:
            print("Received Next Job Execution Changed event. job_id:{} job_document:{}".format(
                execution.job_id, execution.job_document))

            # Start job now, or remember to start it when current job is done
            start_job_now = False
            with locked_data.lock:
                if locked_data.is_working_on_job:
                    locked_data.is_next_job_waiting = True
                else:
                    start_job_now = True

            if start_job_now:
                try_start_next_job()

        else:
            print("Received Next Job Execution Changed event: None. Waiting for further jobs...")

    except Exception as e:
        exit(e)


def on_publish_start_next_pending_job_execution(future):
    # type: (Future) -> None
    try:
        future.result()  # raises exception if publish failed

        print("Published request to start the next job.")

    except Exception as e:
        exit(e)


def on_start_next_pending_job_execution_accepted(response):
    # type: (iotjobs.StartNextJobExecutionResponse) -> None
    try:
        if response.execution:
            execution = response.execution
            print("Request to start next job was accepted. job_id:{} job_document:{}".format(
                execution.job_id, execution.job_document))

            # To emulate working on a job, spawn a thread that sleeps for a few seconds
            job_thread = threading.Thread(
                target=lambda: job_thread_fn(execution.job_id, execution.job_document),
                name='job_thread')
            job_thread.start()
        else:
            print("Request to start next job was accepted, but there are no jobs to be done. Waiting for further jobs ...")
            done_working_on_job()

    except Exception as e:
        exit(e)


def on_start_next_pending_job_execution_rejected(rejected):
    # type: (iotjobs.RejectedError) -> None
    exit("Request to start next pending job rejected with code:'{}' message:'{}'".format(
        rejected.code, rejected.message))


def job_thread_fn(job_id, job_document):
    try:
        print("Starting local work on job...")
        time.sleep(cmdData.input_job_time)
        print("Done working on job.")

        print("Publishing request to update job status to SUCCEEDED...")
        request = iotjobs.UpdateJobExecutionRequest(
            thing_name=jobs_thing_name,
            job_id=job_id,
            status=iotjobs.JobStatus.SUCCEEDED)
        publish_future = jobs_client.publish_update_job_execution(request, mqtt_qos)
        publish_future.add_done_callback(on_publish_update_job_execution)

    except Exception as e:
        exit(e)


def on_publish_update_job_execution(future):
    # type: (Future) -> None
    try:
        future.result()  # raises exception if publish failed
        print("Published request to update job.")

    except Exception as e:
        exit(e)


def on_update_job_execution_accepted(response):
    # type: (iotjobs.UpdateJobExecutionResponse) -> None
    try:
        print("Request to update job was accepted.")
        done_working_on_job()
    except Exception as e:
        exit(e)


def on_update_job_execution_rejected(rejected):
    # type: (iotjobs.RejectedError) -> None
    exit("Request to update job status was rejected. code:'{}' message:'{}'.".format(
        rejected.code, rejected.message))

# MQTT5 specific functions
# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)

# Callback for the lifecycle event on Client Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Client Stopped.")

    # Signal that sample is finished
    is_sample_done.set()

# end MQTT5 specific functions

if __name__ == '__main__':
    # Create the proxy options if the data is present in cmdData

    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    if cmdData.input_mqtt_version == 5:
        mqtt_qos = mqtt5.QoS.AT_LEAST_ONCE
        # Create a mqtt5 connection from the command line data
        mqtt5_client = mqtt5_client_builder.mtls_from_path(
            endpoint=cmdData.input_endpoint,
            port=cmdData.input_port,
            cert_filepath=cmdData.input_cert,
            pri_key_filepath=cmdData.input_key,
            ca_filepath=cmdData.input_ca,
            client_id=cmdData.input_clientId,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_stopped=on_lifecycle_stopped)
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}' with MQTT5...")

        mqtt5_client.start()

        jobs_client = iotjobs.IotJobsClient(mqtt5_client)
        future_connection_success.result()

        # Wait for connection to be fully established.
        # Note that it's not necessary to wait, commands issued to the
        # mqtt5_client before its fully connected will simply be queued.
        # But this sample waits here so it's obvious when a connection
        # fails or succeeds.
    elif cmdData.input_mqtt_version == 3:
        mqtt_qos = mqtt.QoS.AT_LEAST_ONCE
        # Create a MQTT connection from the command line data
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=cmdData.input_endpoint,
            port=cmdData.input_port,
            cert_filepath=cmdData.input_cert,
            pri_key_filepath=cmdData.input_key,
            ca_filepath=cmdData.input_ca,
            client_id=cmdData.input_clientId,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options)

        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}' with MQTT3...")

        connected_future = mqtt_connection.connect()

        jobs_client = iotjobs.IotJobsClient(mqtt_connection)
        connected_future.result()

        # Wait for connection to be fully established.
        # Note that it's not necessary to wait, commands issued to the
        # mqtt_connection before its fully connected will simply be queued.
        # But this sample waits here so it's obvious when a connection
        # fails or succeeds.
    else:
        print("Unsopported MQTT version number\n")
        sys.exit(-1)


    print("Connected!")

    try:
        # List the jobs queued and pending
        get_jobs_request = iotjobs.GetPendingJobExecutionsRequest(thing_name=jobs_thing_name)
        jobs_request_future_accepted, _ = jobs_client.subscribe_to_get_pending_job_executions_accepted(
            request=get_jobs_request,
            qos=mqtt_qos,
            callback=on_get_pending_job_executions_accepted
        )
        # Wait for the subscription to succeed
        jobs_request_future_accepted.result()

        jobs_request_future_rejected, _ = jobs_client.subscribe_to_get_pending_job_executions_rejected(
            request=get_jobs_request,
            qos=mqtt_qos,
            callback=on_get_pending_job_executions_rejected
        )
        # Wait for the subscription to succeed
        jobs_request_future_rejected.result()

        # Get a list of all the jobs
        get_jobs_request_future = jobs_client.publish_get_pending_job_executions(
            request=get_jobs_request,
            qos=mqtt_qos
        )
        # Wait for the publish to succeed
        get_jobs_request_future.result()
    except Exception as e:
        exit(e)
    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".
        print("Subscribing to Next Changed events...")
        changed_subscription_request = iotjobs.NextJobExecutionChangedSubscriptionRequest(
            thing_name=jobs_thing_name)

        subscribed_future, _ = jobs_client.subscribe_to_next_job_execution_changed_events(
            request=changed_subscription_request,
            qos=mqtt_qos,
            callback=on_next_job_execution_changed)

        # Wait for subscription to succeed
        subscribed_future.result()

        print("Subscribing to Start responses...")
        start_subscription_request = iotjobs.StartNextPendingJobExecutionSubscriptionRequest(
            thing_name=jobs_thing_name)
        subscribed_accepted_future, _ = jobs_client.subscribe_to_start_next_pending_job_execution_accepted(
            request=start_subscription_request,
            qos=mqtt_qos,
            callback=on_start_next_pending_job_execution_accepted)

        subscribed_rejected_future, _ = jobs_client.subscribe_to_start_next_pending_job_execution_rejected(
            request=start_subscription_request,
            qos=mqtt_qos,
            callback=on_start_next_pending_job_execution_rejected)

        # Wait for subscriptions to succeed
        subscribed_accepted_future.result()
        subscribed_rejected_future.result()

        print("Subscribing to Update responses...")
        # Note that we subscribe to "+", the MQTT wildcard, to receive
        # responses about any job-ID.
        update_subscription_request = iotjobs.UpdateJobExecutionSubscriptionRequest(
            thing_name=jobs_thing_name,
            job_id='+')

        subscribed_accepted_future, _ = jobs_client.subscribe_to_update_job_execution_accepted(
            request=update_subscription_request,
            qos=mqtt_qos,
            callback=on_update_job_execution_accepted)

        subscribed_rejected_future, _ = jobs_client.subscribe_to_update_job_execution_rejected(
            request=update_subscription_request,
            qos=mqtt_qos,
            callback=on_update_job_execution_rejected)

        # Wait for subscriptions to succeed
        subscribed_accepted_future.result()
        subscribed_rejected_future.result()

        # Make initial attempt to start next job. The service should reply with
        # an "accepted" response, even if no jobs are pending. The response
        # will contain data about the next job, if there is one.
        # (Will do nothing if we are in CI)
        try_start_next_job()

    except Exception as e:
        exit(e)

    # Wait for the sample to finish
    is_sample_done.wait()
