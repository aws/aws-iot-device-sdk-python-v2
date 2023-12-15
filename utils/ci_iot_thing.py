# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import sys

import boto3


def create_iot_thing(thing_name, region, policy_name, certificate_path, key_path, thing_group=None):
    """ Create IoT thing along with policy and credentials. """

    iot_client = boto3.client('iot', region_name=region)

    print(f"Creating thing '{thing_name}'", file=sys.stderr)

    iot_client.create_thing(thingName=thing_name)
    if thing_group:
        iot_client.add_thing_to_thing_group(thingGroupName=thing_group, thingName=thing_name)

    try:
        print("Creating certificate", file=sys.stderr)
        create_cert_response = iot_client.create_keys_and_certificate(
            setAsActive=True
        )

        f = open(certificate_path, "w")
        f.write(create_cert_response['certificatePem'])
        f.close()

        f = open(key_path, "w")
        f.write(create_cert_response['keyPair']['PrivateKey'])
        f.close()

        certificate_arn = create_cert_response['certificateArn']

        print("Attaching policy to certificate", file=sys.stderr)
        iot_client.attach_policy(policyName=policy_name, target=certificate_arn)

        print("Attaching certificate to thing", file=sys.stderr)
        iot_client.attach_thing_principal(thingName=thing_name, principal=certificate_arn)
    except Exception:
        try:
            iot_client.delete_thing(thingName=thing_name)
        except Exception:
            print("ERROR: Could not delete thing", file=sys.stderr)
        raise

    print("IoT thing created successfully", file=sys.stderr)


def delete_iot_thing(thing_name, region):
    """ Delete IoT thing and all its principals. """

    try:
        iot_client = boto3.client('iot', region_name=region)
    except Exception as e:
        print(f"ERROR: Could not make Boto3 client. Credentials likely could not be sourced", file=sys.stderr)
        raise

    # Detach and delete thing's principals.
    try:
        thing_principals = iot_client.list_thing_principals(thingName=thing_name)
        print(f"Detaching and deleting principals: {thing_principals}", file=sys.stderr)
        for principal in thing_principals["principals"]:
            certificate_id = principal.split("/")[1]
            iot_client.detach_thing_principal(thingName=thing_name, principal=principal)
            iot_client.update_certificate(certificateId=certificate_id, newStatus='INACTIVE')
            iot_client.delete_certificate(certificateId=certificate_id, forceDelete=True)
    except Exception:
        print("ERROR: Could not delete certificate for IoT thing {thing_name}, probably thing does not exist",
              file=sys.stderr)
        raise

    # Delete thing.
    try:
        iot_client.delete_thing(thingName=thing_name)
    except Exception:
        raise

    print("IoT thing deleted successfully", file=sys.stderr)

    return 0
