# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
import argparse
from aws_crt import io, mqtt
from awsiot import iotjobs
from concurrent import futures
import sys
import threading
import time
import traceback

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

parser = argparse.ArgumentParser(description="Jobs sample runs all pending job executions.")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"w6zbse3vjd5b4p-ats.iot.us-west-2.amazonaws.com\"")
parser.add_argument('--cert', required=True, help="File path to your client certificate, in PEM format")
parser.add_argument('--key', required=True, help="File path to your private key file, in PEM format")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store")
parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
parser.add_argument('--thing-name', required=True, help="The name assigned to your IoT Thing")
parser.add_argument('--job-time', default=5, type=float, help="Emulate working on job by sleeping this many seconds.")

# Using globals to simplify sample code
connected_future = futures.Future()
is_sample_done = threading.Event()

mqtt_connection = None
jobs_client = None
thing_name = ""

class LockedData(object):
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
            mqtt_connection.disconnect()

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
    request = iotjobs.StartNextPendingJobExecutionRequest(thing_name=args.thing_name)
    publish_future = jobs_client.publish_start_next_pending(request)
    publish_future.add_done_callback(on_publish_start_next_pending)

def done_working_on_job():
    with locked_data.lock:
        locked_data.is_working_on_job = False
        try_again = locked_data.is_next_job_waiting

    if try_again:
        try_start_next_job()

def on_connected(return_code, session_present):
    # type: (int, bool) -> None
    print("Connect completed with code: {}".format(return_code))
    if return_code == 0:
        connected_future.set_result(None)
    else:
        connected_future.set_exception(RuntimeError("Connection failed with code: {}".format(return_code)))

def on_disconnected(return_code):
    # type: (int) -> bool
    print("Disconnected with code: {}".format(return_code))
    with locked_data.lock:
        if locked_data.disconnect_called:
            # Signal that sample is finished
            is_sample_done.set()
            # Don't attempt to reconnect
            return False
        else:
            # Attempt to reconnect
            return True

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

def on_publish_start_next_pending(future):
    # type: (futures.Future) -> None
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
        time.sleep(args.job_time)
        print("Done working on job.")

        print("Publishing request to update job status to SUCCEEDED...")
        request = iotjobs.UpdateJobExecutionRequest(
            thing_name=args.thing_name,
            job_id=job_id,
            status='SUCCEEDED')
        publish_future = jobs_client.publish_update(request)
        publish_future.add_done_callback(on_publish_update)

    except Exception as e:
        exit(e)

def on_publish_update(future):
    # type: (futures.Future) -> None
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
    # Process input args
    args = parser.parse_args()
    thing_name = args.thing_name

    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    client_bootstrap = io.ClientBootstrap(event_loop_group)

    tls_options = io.TlsContextOptions.create_client_with_mtls(args.cert, args.key)
    if args.root_ca:
        tls_options.override_default_trust_store(ca_path=None, ca_file=args.root_ca)
    tls_context = io.ClientTlsContext(tls_options)

    mqtt_client = mqtt.Client(client_bootstrap, tls_context)

    port = 443 if io.is_alpn_available() else 8883
    print("Connecting to {} on port {}...".format(args.endpoint, port))
    mqtt_connection = mqtt.Connection(
            client=mqtt_client,
            client_id=args.client_id)
    mqtt_connection.connect(
            host_name = args.endpoint,
            port = port,
            on_connect=on_connected,
            on_disconnect=on_disconnected,
            use_websocket=False,
            alpn=None,
            clean_session=True,
            keep_alive=6000)

    jobs_client = iotjobs.IotJobsClient(mqtt_connection)

    # Wait for connection to be fully established.
    # Note that it's not necessary to wait, commands issued to the
    # mqtt_connection before its fully connected will simply be queued.
    # But this sample waits here so it's obvious when a connection
    # fails or succeeds.
    connected_future.result()

    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".
        print("Subscribing to Next Changed events...")
        changed_subscription_request = iotjobs.NextJobExecutionChangedEventsSubscriptionRequest(
            thing_name=args.thing_name)

        subscribed_future = jobs_client.subscribe_to_next_changed_events(
            request=changed_subscription_request,
            on_next_job_execution_changed=on_next_job_execution_changed)

        # Wait for subscription to succeed
        subscribed_future.result()

        print("Subscribing to Start responses...")
        start_subscription_request = iotjobs.StartNextPendingJobExecutionSubscriptionRequest(
            thing_name=args.thing_name)
        subscribed_accepted_future = jobs_client.subscribe_to_start_next_pending_accepted(
            request=start_subscription_request,
            on_accepted=on_start_next_pending_job_execution_accepted)

        subscribed_rejected_future = jobs_client.subscribe_to_start_next_pending_rejected(
            request=start_subscription_request,
            on_rejected=on_start_next_pending_job_execution_rejected)

        # Wait for subscriptions to succeed
        subscribed_accepted_future.result()
        subscribed_rejected_future.result()

        print("Subscribing to Update responses...")
        # Note that we subscribe to "+", the MQTT wildcard, to receive
        # responses about any job-ID.
        update_subscription_request = iotjobs.UpdateJobExecutionSubscriptionRequest(
                thing_name=args.thing_name,
                job_id='+')

        subscribed_accepted_future = jobs_client.subscribe_to_update_accepted(
            request=update_subscription_request,
            on_accepted=on_update_job_execution_accepted)

        subscribed_rejected_future = jobs_client.subscribe_to_update_rejected(
            request=update_subscription_request,
            on_rejected=on_update_job_execution_rejected)

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
