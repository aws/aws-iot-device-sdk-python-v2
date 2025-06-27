# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
import pdb
import threading

from awscrt import io, mqtt, mqtt5, mqtt_request_response
from awscrt.mqtt_request_response import SubscriptionStatusEvent, SubscriptionStatusEventType

import awsiot
from awsiot import iotjobs

import boto3
from botocore.exceptions import ClientError
from concurrent.futures import Future
import os
import time
import unittest
import uuid


TIMEOUT = 30.0


def create_client_id():
    return f"test-{uuid.uuid4().hex}"


def _get_env_variable(env_name):
    env_data = os.environ.get(env_name)
    if not env_data:
        raise unittest.SkipTest(f"test requires env var: {env_name}")
    return env_data


class JobsTestCallbacks():
    def __init__(self):
        self.future_connection_success = Future()
        self.future_stopped = Future()

    def ws_handshake_transform(self, transform_args):
        transform_args.set_done()

    def on_publish_received(self, publish_received_data: mqtt5.PublishReceivedData):
        pass

    def on_lifecycle_stopped(self, lifecycle_stopped: mqtt5.LifecycleStoppedData):
        if self.future_stopped:
            self.future_stopped.set_result(None)

    def on_lifecycle_attempting_connect(self, lifecycle_attempting_connect: mqtt5.LifecycleAttemptingConnectData):
        pass

    def on_lifecycle_connection_success(self, lifecycle_connection_success: mqtt5.LifecycleConnectSuccessData):
        if self.future_connection_success:
            self.future_connection_success.set_result(lifecycle_connection_success)

    def on_lifecycle_connection_failure(self, lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
        if self.future_connection_success:
            if self.future_connection_success.done():
                pass
            else:
                self.future_connection_success.set_exception(lifecycle_connection_failure.exception)

    def on_lifecycle_disconnection(self, lifecycle_disconnect_data: mqtt5.LifecycleDisconnectData):
        pass

class TestContext():
    def __init__(self):
        self.region = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_REGION")
        self.iot_client = boto3.client('iot', self.region)
        self.thing_name = None
        self.thing_group_name = None
        self.thing_group_arn = None
        self.job_id = None
        self.job_executions_changed_events = []
        self.next_job_execution_changed_events = []
        self.lock = threading.Lock()
        self.signal = threading.Condition(lock=self.lock)

class JobsServiceTest(unittest.TestCase):

    def _create_protocol_client5(self):

        input_host_name = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_HOST")
        input_cert = _get_env_variable("AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_MQTT5_IOT_KEY_PATH")

        client_options = mqtt5.ClientOptions(
            host_name=input_host_name,
            port=8883
        )

        tls_ctx_options = io.TlsContextOptions.create_client_with_mtls_from_path(
            input_cert,
            input_key
        )
        client_options.tls_ctx = io.ClientTlsContext(tls_ctx_options)

        client_options.connect_options = mqtt5.ConnectPacket()
        client_options.connect_options.client_id = create_client_id()

        callbacks = JobsTestCallbacks()
        client_options.on_lifecycle_event_stopped_fn = callbacks.on_lifecycle_stopped
        client_options.on_lifecycle_event_connection_success_fn = callbacks.on_lifecycle_connection_success
        client_options.on_lifecycle_event_connection_failure_fn = callbacks.on_lifecycle_connection_failure
        client_options.on_lifecycle_event_stopped_fn = callbacks.on_lifecycle_stopped

        protocol_client = mqtt5.Client(client_options)
        protocol_client.start()

        callbacks.future_connection_success.result(TIMEOUT)

        return protocol_client, callbacks

    def _shutdown_protocol_client5(self, protocol_client, callbacks):

        protocol_client.stop()
        callbacks.future_stopped.result(TIMEOUT)

    def _create_protocol_client311(self):

        input_host_name = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_HOST")
        input_cert = _get_env_variable("AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_MQTT5_IOT_KEY_PATH")

        tls_ctx_options = io.TlsContextOptions.create_client_with_mtls_from_path(
            input_cert,
            input_key
        )
        tls_ctx = io.ClientTlsContext(tls_ctx_options)

        client = mqtt.Client(None, tls_ctx)

        protocol_client = mqtt.Connection(
            client=client,
            client_id=create_client_id(),
            host_name=input_host_name,
            port=8883,
            ping_timeout_ms=10000,
            keep_alive_secs=30
        )
        protocol_client.connect().result(TIMEOUT)

        return protocol_client

    def _shutdown_protocol_client311(self, protocol_client):
        protocol_client.disconnect().result(TIMEOUT)

    def _create_jobs_client(
            self,
            protocol_client,
            max_request_response_subscriptions,
            max_streaming_subscriptions,
            operation_timeout_seconds):
        rr_client_options = mqtt_request_response.ClientOptions(
            max_request_response_subscriptions, max_streaming_subscriptions)
        rr_client_options.operation_timeout_in_seconds = operation_timeout_seconds

        jobs_client = iotjobs.IotJobsClientV2(protocol_client, rr_client_options)

        return jobs_client

    def _do_jobs_creation_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()

        test_callable(protocol_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_jobs_creation_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()

        test_callable(protocol_client)

        self._shutdown_protocol_client311(protocol_client)

    def _do_jobs_operation_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()
        identity_client = self._create_jobs_client(protocol_client, 2, 2, 30)

        test_callable(identity_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_jobs_operation_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()
        identity_client = self._create_jobs_client(protocol_client, 2, 2, 30)

        test_callable(identity_client)

        self._shutdown_protocol_client311(protocol_client)

    def _tear_down(self, test_context):
        if test_context.iot_client is None:
            return

        if test_context.job_id is not None:
            done = False
            while not done:
                try:
                    test_context.iot_client.delete_job(jobId=test_context.job_id, force=True)
                    done=True
                except ClientError as ce:
                    exception_type = ce.response['Error']['Code']
                    if exception_type == 'ThrottlingException' or exception_type == 'LimitExceededException':
                        time.sleep(10)
                    elif exception_type == 'ResourceNotFoundException':
                        done = True


        if test_context.thing_name is not None:
            test_context.iot_client.delete_thing(thingName=test_context.thing_name)

        if test_context.thing_group_name is not None:
            test_context.iot_client.delete_thing_group(thingGroupName=test_context.thing_group_name)

    def _setup(self, test_context):
        tgn = "tgn-" + uuid.uuid4().hex

        create_tg_response = test_context.iot_client.create_thing_group(thingGroupName=tgn)

        test_context.thing_group_name = tgn
        test_context.thing_group_arn = create_tg_response['thingGroupArn']

        thing_name = "thing-" + uuid.uuid4().hex

        test_context.iot_client.create_thing(thingName=thing_name)
        test_context.thing_name = thing_name

        time.sleep(1)

        job_id = "job-" + uuid.uuid4().hex
        job_document = '{"test":"do-something"}'

        test_context.iot_client.create_job(
            jobId=job_id,
            document=job_document,
            targets=[test_context.thing_group_arn],
            targetSelection='CONTINUOUS')

        test_context.job_id = job_id

    def _create_job_executions_changed_stream(self, test_context, jobs_client):
        subscribed = Future()

        def on_incoming_publish_event(event):
            with test_context.signal:
                test_context.job_executions_changed_events.append(event)
                test_context.signal.notify_all()

        def on_subscription_event(event : SubscriptionStatusEvent):
            if event.type == SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED:
                subscribed.set_result(event)

        stream_options = awsiot.ServiceStreamOptions(
            incoming_event_listener=on_incoming_publish_event,
            subscription_status_listener=on_subscription_event
        )

        stream = jobs_client.create_job_executions_changed_stream(
            iotjobs.JobExecutionsChangedSubscriptionRequest(thing_name=test_context.thing_name),
            stream_options)
        stream.open()

        subscription_event = subscribed.result(TIMEOUT)
        self.assertEqual(mqtt_request_response.SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED,
                         subscription_event.type)

        return stream

    def _create_next_job_execution_changed_stream(self, test_context, jobs_client):
        subscribed = Future()

        def on_incoming_publish_event(event):
            with test_context.signal:
                test_context.next_job_execution_changed_events.append(event)
                test_context.signal.notify_all()

        def on_subscription_event(event : SubscriptionStatusEvent):
            if event.type == SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED:
                subscribed.set_result(event)

        stream_options = awsiot.ServiceStreamOptions(
            incoming_event_listener=on_incoming_publish_event,
            subscription_status_listener=on_subscription_event
        )

        stream = jobs_client.create_next_job_execution_changed_stream(
            iotjobs.NextJobExecutionChangedSubscriptionRequest(thing_name=test_context.thing_name),
            stream_options)
        stream.open()

        subscription_event = subscribed.result(TIMEOUT)
        self.assertEqual(mqtt_request_response.SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED,
                         subscription_event.type)

        return stream

    def _wait_for_initial_stream_events(self, test_context):
        with test_context.signal:
            while len(test_context.next_job_execution_changed_events) == 0:
                test_context.signal.wait()

            next_job_execution_changed_event = test_context.next_job_execution_changed_events[0]
            self.assertEqual(test_context.job_id, next_job_execution_changed_event.execution.job_id)
            self.assertEqual(iotjobs.JobStatus.QUEUED, next_job_execution_changed_event.execution.status)

            while len(test_context.job_executions_changed_events) == 0:
                test_context.signal.wait()

            job_executions_changed_event = test_context.job_executions_changed_events[0]
            queued_jobs = job_executions_changed_event.jobs[iotjobs.JobStatus.QUEUED]
            self.assertTrue(len(queued_jobs) > 0)
            self.assertEqual(test_context.job_id, queued_jobs[0].job_id)

    def _wait_for_final_stream_events(self, test_context):
        with test_context.signal:
            while len(test_context.next_job_execution_changed_events) < 2:
                test_context.signal.wait()

            final_next_job_execution_changed_event = test_context.next_job_execution_changed_events[1]
            self.assertIsNotNone(final_next_job_execution_changed_event.timestamp)
            self.assertIsNone(final_next_job_execution_changed_event.execution)

            while len(test_context.job_executions_changed_events) < 2:
                test_context.signal.wait()

            final_job_executions_changed_event = test_context.job_executions_changed_events[1]
            self.assertTrue(final_job_executions_changed_event.jobs == None or
                            len(final_job_executions_changed_event.jobs) == 0)

    def _verify_nothing_in_progress(self, test_context, jobs_client):
        get_pending_response = jobs_client.get_pending_job_executions(
            iotjobs.GetPendingJobExecutionsRequest(
                thing_name=test_context.thing_name
            )
        ).result(TIMEOUT)

        self.assertEqual(0, len(get_pending_response.queued_jobs))
        self.assertEqual(0, len(get_pending_response.in_progress_jobs))

    def _do_job_processing_test(self, jobs_client):
        test_context = TestContext()
        try:
            self._setup(test_context)
            job_executions_changed_stream = self._create_job_executions_changed_stream(test_context, jobs_client)
            next_job_execution_changed_stream = self._create_next_job_execution_changed_stream(test_context, jobs_client)

            self._verify_nothing_in_progress(test_context, jobs_client)

            test_context.iot_client.add_thing_to_thing_group(
                thingName=test_context.thing_name,
                thingGroupName=test_context.thing_group_name
            )

            self._wait_for_initial_stream_events(test_context)

            # start the job
            start_next_response = jobs_client.start_next_pending_job_execution(
                iotjobs.StartNextPendingJobExecutionRequest(thing_name=test_context.thing_name)
            ).result(TIMEOUT)

            self.assertEqual(test_context.job_id, start_next_response.execution.job_id)

            # pretend to do the job
            time.sleep(1)

            # verify in progress
            describe_job_response = jobs_client.describe_job_execution(
                iotjobs.DescribeJobExecutionRequest(
                    job_id=test_context.job_id,
                    thing_name=test_context.thing_name
                )
            ).result(TIMEOUT)

            self.assertEqual(test_context.job_id, describe_job_response.execution.job_id)
            self.assertEqual(iotjobs.JobStatus.IN_PROGRESS, describe_job_response.execution.status)

            # complete the job
            jobs_client.update_job_execution(iotjobs.UpdateJobExecutionRequest(
                job_id=test_context.job_id,
                thing_name=test_context.thing_name,
                status=iotjobs.JobStatus.SUCCEEDED
            )).result(TIMEOUT)

            self._wait_for_final_stream_events(test_context)
            self._verify_nothing_in_progress(test_context, jobs_client)

        finally:
            self._tear_down(test_context)

    # ==============================================================
    #             CREATION SUCCESS TEST CASES
    # ==============================================================
    def test_client_creation_success5(self):
        self._do_jobs_creation_test5(lambda protocol_client: self._create_jobs_client(protocol_client, 2, 2, 30))

    def test_client_creation_success311(self):
        self._do_jobs_creation_test311(lambda protocol_client: self._create_jobs_client(protocol_client, 2, 2, 30))

    # ==============================================================
    #             CREATION FAILURE TEST CASES
    # ==============================================================
    def test_client_creation_failure_no_protocol_client(self):
        self.assertRaises(Exception, self._create_jobs_client, None, 2, 2, 30)

    # ==============================================================
    #             REQUEST RESPONSE OPERATION TEST CASES
    # ==============================================================
    def test_job_processing5(self):
        self._do_jobs_operation_test5(lambda jobs_client: self._do_job_processing_test(jobs_client))

    def test_job_processing311(self):
        self._do_jobs_operation_test311(lambda jobs_client: self._do_job_processing_test(jobs_client))

if __name__ == 'main':
    unittest.main()
