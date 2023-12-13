# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
import json
import os
import sys
import uuid
import time

import boto3

import run_in_ci
import ci_iot_thing


def main():
    argument_parser = argparse.ArgumentParser(
        description="Run Jobs test in CI")
    argument_parser.add_argument(
        "--config-file", required=True, help="JSON file providing command-line arguments for a test")
    argument_parser.add_argument(
        "--input-uuid", required=False, help="UUID for thing name. UUID will be generated if this option is omit")
    argument_parser.add_argument(
        "--region", required=False, default="us-east-1", help="The name of the region to use")
    parsed_commands = argument_parser.parse_args()

    try:
        iot_client = boto3.client('iot', region_name=parsed_commands.region)
        secrets_client = boto3.client("secretsmanager", region_name=parsed_commands.region)
    except Exception as e:
        print(f"ERROR: Could not make Boto3 iot-data client. Credentials likely could not be sourced. Exception: {e}",
              file=sys.stderr)
        return -1

    input_uuid = parsed_commands.input_uuid if parsed_commands.input_uuid else str(uuid.uuid4())

    thing_name = "ServiceTest_Jobs_" + input_uuid
    policy_name = secrets_client.get_secret_value(
        SecretId="ci/JobsServiceClientTest/policy_name")["SecretString"]

    # Temporary certificate/key file path.
    certificate_path = os.path.join(os.getcwd(), "tests/JobsExecution/certificate.pem.crt")
    key_path = os.path.join(os.getcwd(), "tests/JobsExecution/private.pem.key")

    try:
        ci_iot_thing.create_iot_thing(
            thing_name=thing_name,
            thing_group="CI_ServiceClient_Thing_Group",
            region=parsed_commands.region,
            policy_name=policy_name,
            certificate_path=certificate_path,
            key_path=key_path)
    except Exception as e:
        print(f"ERROR: Failed to create IoT thing: {e}")
        sys.exit(-1)

    thing_job = 'ERROR'
    i = 0;
    while 'ERROR' in thing_job and i <= 4:
        try:
            job_id = secrets_client.get_secret_value(SecretId="ci/JobsServiceClientTest/job_id")["SecretString"]
            thing_job = iot_client.describe_job_execution(jobId=job_id, thingName=thing_name)
            print(f'thing job is {thing_job}');
            if 'ERROR' in thing_job:
               i = i + 1;
            else:
                break;
        except Exception as e:
            print(f"Waiting for a newly created thing to be ready for the Job {e}")
            i = i + 1;
        time.sleep(1);

    # Perform Jobs test. If it's successful, the Job execution should be marked as SUCCEEDED for the thing.
    try:
        test_result = run_in_ci.setup_and_launch(parsed_commands.config_file, input_uuid)
    except Exception as e:
        print(f"ERROR: Failed to execute Jobs test: {e}")
        test_result = -1

    # Test reported success, verify that Job was indeed executed by the thing.
    if test_result == 0:
        print("Verifying that Job was executed")
        try:
            job_id = secrets_client.get_secret_value(SecretId="ci/JobsServiceClientTest/job_id")["SecretString"]
            thing_job = iot_client.describe_job_execution(jobId=job_id, thingName=thing_name)
            job_status = thing_job.get('execution', {}).get('status', {})
            if job_status != 'SUCCEEDED':
                print(f"ERROR: Could not verify Job execution; Job info: {thing_job}")
                test_result = -1
        except Exception as e:
            print(f"ERROR: Could not verify Job execution: {e}")
            test_result = -1

    if test_result == 0:
        print("Test succeeded")

    # Delete a thing created for this test run.
    # NOTE We want to try to delete thing even if test was unsuccessful.
    try:
        ci_iot_thing.delete_iot_thing(thing_name, parsed_commands.region)
    except Exception as e:
        print(f"ERROR: Failed to delete thing: {e}")
        # Fail the test if unable to delete thing, so this won't remain unnoticed.
        test_result = -1

    try:
        if os.path.isfile(certificate_path):
            os.remove(certificate_path)
        if os.path.isfile(key_path):
            os.remove(key_path)
    except Exception as e:
        print(f"WARNING: Failed to delete local files: {e}")

    if test_result != 0:
        sys.exit(-1)


if __name__ == "__main__":
    main()
