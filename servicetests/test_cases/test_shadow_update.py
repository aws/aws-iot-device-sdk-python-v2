# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-3.0.

import argparse
import json
import os
import sys
import uuid
import time

import boto3

import run_in_ci
import ci_iot_thing


def get_shadow_attrs(config_file):
    with open(config_file) as f:
        json_data = json.load(f)
        shadow_name = next((json_arg["data"] for json_arg in json_data["arguments"] if json_arg.get("name", "") == "--shadow_name"), "")
        shadow_property = next((json_arg["data"] for json_arg in json_data["arguments"] if json_arg.get("name", "") == "--shadow_property"), "")
        shadow_desired_value = next((json_arg["data"] for json_arg in json_data["arguments"] if json_arg.get("name", "") == "--shadow_value"), "")
        return [shadow_name, shadow_property, shadow_desired_value]


def main():
    argument_parser = argparse.ArgumentParser(
        description="Run Shadow test in CI")
    argument_parser.add_argument(
        "--config-file", required=True,
        help="JSON file providing command-line arguments for a test")
    argument_parser.add_argument(
        "--input-uuid", required=False, help="UUID for thing name. UUID will be generated if this option is omit")
    argument_parser.add_argument(
        "--region", required=False, default="us-east-1", help="The name of the region to use")
    parsed_commands = argument_parser.parse_args()

    [shadow_name, shadow_property, shadow_desired_value] = get_shadow_attrs(parsed_commands.config_file)
    print(f"Shadow name: '{shadow_name}'")
    print(f"Shadow property: '{shadow_property}'")
    print(f"Shadow desired value: '{shadow_desired_value}'")

    try:
        iot_data_client = boto3.client('iot-data', region_name=parsed_commands.region)
        secrets_client = boto3.client("secretsmanager", region_name=parsed_commands.region)
    except Exception as e:
        print(f"ERROR: Could not make Boto3 iot-data client. Credentials likely could not be sourced. Exception: {e}",
              file=sys.stderr)
        return -1

    input_uuid = parsed_commands.input_uuid if parsed_commands.input_uuid else str(uuid.uuid4())

    thing_name = "ServiceTest_Shadow_" + input_uuid
    policy_name = secrets_client.get_secret_value(
        SecretId="ci/ShadowServiceClientTest/policy_name")["SecretString"]

    # Temporary certificate/key file path.
    certificate_path = os.path.join(os.getcwd(), "tests/ShadowUpdate/certificate.pem.crt")
    key_path = os.path.join(os.getcwd(), "tests/ShadowUpdate/private.pem.key")

    try:
        ci_iot_thing.create_iot_thing(
            thing_name=thing_name,
            region=parsed_commands.region,
            policy_name=policy_name,
            certificate_path=certificate_path,
            key_path=key_path)
    except Exception as e:
        print(f"ERROR: Failed to create IoT thing: {e}")
        sys.exit(-1)

    # Perform Shadow test. If it's successful, a shadow should appear for a specified thing.
    try:
        test_result = run_in_ci.setup_and_launch(parsed_commands.config_file, input_uuid)
    except Exception as e:
        print(f"ERROR: Failed to execute Jobs test: {e}")
        test_result = -1

    # Test reported success, verify that shadow was indeed updated.
    if test_result == 0:
        print("Verifying that shadow was updated")
        shadow_value = None
        try:
            if shadow_name:
                thing_shadow = iot_data_client.get_thing_shadow(thingName=thing_name, shadowName=shadow_name)
            else:
                thing_shadow = iot_data_client.get_thing_shadow(thingName=thing_name)

            payload = thing_shadow['payload'].read()
            data = json.loads(payload)
            shadow_value = data.get('state', {}).get('reported', {}).get(shadow_property, None)
            if shadow_value != shadow_desired_value:
                print(f"ERROR: Could not verify thing shadow: {shadow_property} is not set to desired value "
                      f"'{shadow_desired_value}'; shadow actual state: {data}")
                test_result = -1
        except KeyError as e:
            print(f"ERROR: Could not verify thing shadow: key {e} does not exist in shadow response: {thing_shadow}")
            test_result = -1
        except Exception as e:
            print(f"ERROR: Could not verify thing shadow: {e}")
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
