# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# Built-in
import argparse
import sys
# Needs to be installed via pip
import boto3  # - for launching sample

def DeleteIoTThing(parsed_commands):
    try:
        iot_client = boto3.client('iot', region_name=parsed_commands.region)
    except Exception:
        print("Error - could not make Boto3 client. Credentials likely could not be sourced")
        return -1

    thing_principals = None
    try:
        thing_principals = iot_client.list_thing_principals(thingName=parsed_commands.thing_name)
    except Exception:
        print ("Could not get thing principals!")
        return -1

    try:
        if (thing_principals != None):
            if (thing_principals["principals"] != None):
                if (len(thing_principals["principals"]) > 0 and parsed_commands.delete_certificate == "true"):
                    for principal in thing_principals["principals"]:
                        certificate_id = principal.split("/")[1]
                        iot_client.detach_thing_principal(thingName=parsed_commands.thing_name, principal=principal)
                        iot_client.update_certificate(certificateId=certificate_id, newStatus ='INACTIVE')
                        iot_client.delete_certificate(certificateId=certificate_id, forceDelete=True)
    except Exception as exception:
        print (exception)
        print ("Could not delete certificate!")
        return -1

    try:
        iot_client.delete_thing(thingName=parsed_commands.thing_name)
    except Exception as exception:
        print (exception)
        print ("Could not delete IoT thing!")
        return -1

    print ("IoT thing deleted successfully")
    return 0



def main():
    argument_parser = argparse.ArgumentParser(
        description="Delete IoT Thing")
    argument_parser.add_argument("--thing_name", metavar="<The name of the IoT thing to delete>", required=True,
                                 help="The name of the IoT thing to delete")
    argument_parser.add_argument("--region", metavar="<Name of region>",
                                 required=True, default="us-east-1", help="The name of the region to use")
    argument_parser.add_argument("--delete_certificate", metavar="<Set to 'true' to delete the certificate. Is set to 'true' by default>",
                                 required=False, default="true", help="Will delete the certificate after detaching it from the IoT thing")
    parsed_commands = argument_parser.parse_args()

    print ("Deleting IoT thing...")
    delete_result = DeleteIoTThing(parsed_commands)
    sys.exit(delete_result)


if __name__ == "__main__":
    main()
