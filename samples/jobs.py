# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import auth, http, io, mqtt
from awsiot import iotjobs
from awsiot import mqtt_connection_builder
from concurrent.futures import Future
import sys
import threading
import time
import traceback
from uuid import uuid4

# - Overview -
# This sample uses the AWS IoT Jobs Service to receive and execute operations
# on the device. Imagine periodic software updates that must be sent to and
# executed on devices in the wild.
#
# - Instructions -
# This sample requires you to create jobs for your device to execute. See:
# https://docs.aws.amazon.com/iot/latest/developerguide/create-manage-jobs.html
#
# - Detail -
# On startup, the sample tries to start the next pending job execution.
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

# Parse arguments
import command_line_utils;
cmdUtils = command_line_utils.CommandLineUtils("Jobs - Recieve and execute operations on the device.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command("client_id", "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
cmdUtils.register_command("port", "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
cmdUtils.register_command("thing_name", "<str>", "The name assigned to your IoT Thing", required=True)
cmdUtils.register_command("job_time", "<int>", "Emulate working on a job by sleeping this many seconds (optional, default='5')", default=5, type=int)
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

mqtt_connection = None
jobs_client = None
jobs_thing_name = cmdUtils.get_command_required("thing_name")

class LockedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.disconnect_called = False
        self.is_working_on_job = False
        self.is_next_job_waiting = False

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
    publish_future = jobs_client.publish_start_next_pending_job_execution(request, mqtt.QoS.AT_LEAST_ONCE)
    publish_future.add_done_callback(on_publish_start_next_pending_job_execution)

def done_working_on_job():
    with locked_data.lock:
        locked_data.is_working_on_job = False
        try_again = locked_data.is_next_job_waiting

    if try_again:
        try_start_next_job()

def on_disconnected(disconnect_future):
    # type: (Future) -> None
    print("Disconnected.")

    # Signal that sample is finished
    is_sample_done.set()

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
        future.result() # raises exception if publish failed

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
            print("Request to start next job was accepted, but there are no jobs to be done. Waiting for further jobs...")
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
        time.sleep(cmdUtils.get_command("job_time"))
        print("Done working on job.")

        print("Publishing request to update job status to SUCCEEDED...")
        request = iotjobs.UpdateJobExecutionRequest(
            thing_name=jobs_thing_name,
            job_id=job_id,
            status=iotjobs.JobStatus.SUCCEEDED)
        publish_future = jobs_client.publish_update_job_execution(request, mqtt.QoS.AT_LEAST_ONCE)
        publish_future.add_done_callback(on_publish_update_job_execution)

    except Exception as e:
        exit(e)

def on_publish_update_job_execution(future):
    # type: (Future) -> None
    try:
        future.result() # raises exception if publish failed
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

if __name__ == '__main__':
    mqtt_connection = cmdUtils.build_mqtt_connection(None, None)
    print("Connecting to {} with client ID '{}'...".format(
        cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))

    connected_future = mqtt_connection.connect()

    jobs_client = iotjobs.IotJobsClient(mqtt_connection)

    # Wait for connection to be fully established.
    # Note that it's not necessary to wait, commands issued to the
    # mqtt_connection before its fully connected will simply be queued.
    # But this sample waits here so it's obvious when a connection
    # fails or succeeds.
    connected_future.result()
    print("Connected!")

    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".
        print("Subscribing to Next Changed events...")
        changed_subscription_request = iotjobs.NextJobExecutionChangedSubscriptionRequest(
            thing_name=jobs_thing_name)

        subscribed_future, _ = jobs_client.subscribe_to_next_job_execution_changed_events(
            request=changed_subscription_request,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_next_job_execution_changed)

        # Wait for subscription to succeed
        subscribed_future.result()

        print("Subscribing to Start responses...")
        start_subscription_request = iotjobs.StartNextPendingJobExecutionSubscriptionRequest(
            thing_name=jobs_thing_name)
        subscribed_accepted_future, _ = jobs_client.subscribe_to_start_next_pending_job_execution_accepted(
            request=start_subscription_request,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_start_next_pending_job_execution_accepted)

        subscribed_rejected_future, _ = jobs_client.subscribe_to_start_next_pending_job_execution_rejected(
            request=start_subscription_request,
            qos=mqtt.QoS.AT_LEAST_ONCE,
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
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_update_job_execution_accepted)

        subscribed_rejected_future, _ = jobs_client.subscribe_to_update_job_execution_rejected(
            request=update_subscription_request,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_update_job_execution_rejected)

        # Wait for subscriptions to succeed
        subscribed_accepted_future.result()
        subscribed_rejected_future.result()

        # Make initial attempt to start next job. The service should reply with
        # an "accepted" response, even if no jobs are pending. The response
        # will contain data about the next job, if there is one.
        try_start_next_job()

    except Exception as e:
        exit(e)

    # Wait for the sample to finish
    is_sample_done.wait()
