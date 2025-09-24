# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import iotjobs, mqtt5_client_builder
from awscrt import mqtt5, mqtt_request_response
import boto3
from concurrent.futures import Future
from dataclasses import dataclass
from typing import Optional
import awsiot, sys

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse

parser = argparse.ArgumentParser(
    description="AWS IoT Jobs sandbox application")
required = parser.add_argument_group("required arguments")

# Required Arguments
required.add_argument('--endpoint',  metavar="", required=True,
                      help="AWS IoT endpoint to connect to")
required.add_argument('--cert',  metavar="", required=True,
                    help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument('--key',  metavar="", required=True,
                    help="Path to the private key file to use during mTLS connection establishment")
required.add_argument('--thing',  metavar="", required=True,
                    help="Name of the IoT thing to interact with")
required.add_argument('--region',  metavar="", required=True,
                    help="AWS region to use.  Must match the endpoint region.")

args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


@dataclass
class SampleContext:
    jobs_client: 'iotjobs.IotJobsClientV2'
    thing: 'str'
    thing_arn: Optional['str']
    region: 'str'
    control_plane_client: any

def print_help():
    print("Jobs Sandbox\n")
    print('IoT control plane commands:');
    print('  create-job <jobId> <job-document-as-json> -- create a new job with the specified job id and (JSON) document');
    print('  delete-job <jobId> -- deletes a job with the specified job id');
    print('MQTT Jobs service commands:');
    print('  describe-job-execution <jobId> -- gets the service status of a job execution with the specified job id');
    print('  get-pending-job-executions -- gets all incomplete job executions');
    print('  start-next-pending-job-execution -- moves the next pending job execution into the IN_PROGRESS state');
    print('  update-job-execution <jobId> <SUCCEEDED | IN_PROGRESS | FAILED | CANCELED> -- updates a job execution with a new status');
    print('Miscellaneous commands:')
    print("  quit - quits the sample application\n");
    pass

def handle_create_job(context : SampleContext, parameters: str):
    params = parameters.strip().split(" ", 1)
    job_id = params[0]
    job_document = params[1]

    create_response = context.control_plane_client.create_job(
        jobId=job_id,
        document=job_document,
        targets=[context.thing_arn],
        targetSelection='SNAPSHOT')
    print(f"CreateJobResponse: {create_response}\n")

def handle_delete_job(context : SampleContext, parameters: str):
    job_id = parameters.strip()
    delete_response = context.control_plane_client.delete_job(jobId=job_id, force=True)
    print(f"DeleteJobResponse: {delete_response}\n")

def handle_describe_job_execution(context : SampleContext, parameters: str):
    job_id = parameters.strip()
    describe_response = context.jobs_client.describe_job_execution(iotjobs.DescribeJobExecutionRequest(job_id=job_id, thing_name=context.thing)).result()
    print(f"DescribeJobExecutionResponse: {describe_response}\n")

def handle_get_pending_job_executions(context : SampleContext):
    get_response = context.jobs_client.get_pending_job_executions(iotjobs.GetPendingJobExecutionsRequest(thing_name=context.thing)).result()
    print(f"GetPendingJobExecutionsResponse: {get_response}\n")

def handle_start_next_pending_job_execution(context : SampleContext):
    start_response = context.jobs_client.start_next_pending_job_execution(iotjobs.StartNextPendingJobExecutionRequest(thing_name=context.thing)).result()
    print(f"StartNextPendingJobExecutionResponse: {start_response}\n")

def handle_update_job_execution(context : SampleContext, parameters: str):
    params = parameters.strip().split(" ", 1)
    job_id = params[0]
    status = params[1]
    update_response = context.jobs_client.update_job_execution(iotjobs.UpdateJobExecutionRequest(thing_name=context.thing, job_id=job_id, status=status)).result()
    print(f"UpdateJobExecutionResponse: {update_response}\n")

def handle_input(context : SampleContext, line: str):
    words = line.strip().split(" ", 1)
    command = words[0]

    if command == "quit":
        return True
    elif command == "create-job":
        handle_create_job(context, words[1])
    elif command == "delete-job":
        handle_delete_job(context, words[1])
    elif command == "describe-job-execution":
        handle_describe_job_execution(context, words[1])
    elif command == "get-pending-job-executions":
        handle_get_pending_job_executions(context)
    elif command == "start-next-pending-job-execution":
        handle_start_next_pending_job_execution(context)
    elif command == "update-job-execution":
        handle_update_job_execution(context, words[1])
    else:
        print_help()

    return False

def create_thing_if_needed(context: SampleContext):
    try:
        describe_response = context.control_plane_client.describe_thing(thingName=context.thing)
        context.thing_arn = describe_response['thingArn']
        return
    except:
        pass

    print(f"Thing {context.thing} not found, creating...")

    create_response = context.control_plane_client.create_thing(thingName=context.thing)
    context.thing_arn = create_response['thingArn']

    print(f"Thing {context.thing} successfully created with arn {context.thing_arn}")

if __name__ == '__main__':
    initial_connection_success = Future()
    def on_lifecycle_connection_success(event: mqtt5.LifecycleConnectSuccessData):
        initial_connection_success.set_result(True)

    def on_lifecycle_connection_failure(event: mqtt5.LifecycleConnectFailureData):
        initial_connection_success.set_exception(Exception("Failed to connect"))

    def on_lifecycle_disconnection(event: mqtt5.LifecycleDisconnectData):
        print("Lifecycle Disconnected with reason code:{}".format(
            event.disconnect_packet.reason_code if event.disconnect_packet else "None"))

    stopped = Future()
    def on_lifecycle_stopped(event: mqtt5.LifecycleStoppedData):
        stopped.set_result(True)

    # Create a mqtt5 connection from the command line data
    mqtt5_client = mqtt5_client_builder.mtls_from_path(
        endpoint=args.endpoint,
        port=8883,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        clean_session=True,
        keep_alive_secs=1200,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        on_lifecycle_disconnection=on_lifecycle_disconnection,
        on_lifecycle_stopped=on_lifecycle_stopped)

    mqtt5_client.start()

    rr_options = mqtt_request_response.ClientOptions(
        max_request_response_subscriptions = 2,
        max_streaming_subscriptions = 2,
        operation_timeout_in_seconds = 30,
    )
    jobs_client = iotjobs.IotJobsClientV2(mqtt5_client, rr_options)

    initial_connection_success.result()
    print("Connected!")

    def on_job_executions_changed_event(event: iotjobs.JobExecutionsChangedEvent):
        print(f"Received JobExecutionsChangedEvent:\n  {event}\n");

    stream_options = awsiot.ServiceStreamOptions(
        incoming_event_listener=on_job_executions_changed_event,
    )

    job_executions_changed_stream = jobs_client.create_job_executions_changed_stream(
        iotjobs.JobExecutionsChangedSubscriptionRequest(thing_name=args.thing),
        stream_options)
    job_executions_changed_stream.open()

    def on_next_job_execution_changed_event(event: iotjobs.NextJobExecutionChangedEvent):
        print(f"Received NextJobExecutionChangedEvent:\n  {event}\n");

    stream_options = awsiot.ServiceStreamOptions(
        incoming_event_listener=on_next_job_execution_changed_event,
    )

    next_job_execution_changed_stream = jobs_client.create_next_job_execution_changed_stream(
        iotjobs.NextJobExecutionChangedSubscriptionRequest(thing_name=args.thing),
        stream_options)
    next_job_execution_changed_stream.open()

    boto3_client = boto3.client('iot', args.region)
    context = SampleContext(jobs_client, args.thing, None, args.region, boto3_client)

    create_thing_if_needed(context)

    for line in sys.stdin:
        try:
            if handle_input(context, line):
                break

        except Exception as e:
            print(f"Exception: {e}\n")

    mqtt5_client.stop()
    stopped.result()
    print("Stopped!")



