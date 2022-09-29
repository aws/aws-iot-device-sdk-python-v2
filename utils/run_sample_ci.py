# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# Built-in
import argparse
import os
import subprocess
import pathlib
import sys
# Needs to be installed via pip
import boto3  # - for launching sample


current_folder = pathlib.Path(__file__).resolve()
tmp_certificate_file_path = str(current_folder) + "tmp_certificate.pem"
tmp_private_key_path = str(current_folder) + "tmp_privatekey.pem.key"


def getSecretsAndLaunch(parsed_commands):
    global tmp_certificate_file_path
    global tmp_private_key_path
    exit_code = 0
    sample_endpoint = ""
    sample_certificate = ""
    sample_private_key = ""
    sample_custom_authorizer_name = ""
    sample_custom_authorizer_password = ""

    current_folder = pathlib.Path(__file__).resolve()
    # Remove the name of the python file
    current_folder = str(current_folder).replace("run_sample_ci.py", "")

    print("Attempting to get credentials from secrets using Boto3...")
    secrets_client = boto3.client(
        "secretsmanager", region_name=parsed_commands.sample_region)
    try:
        if (parsed_commands.sample_secret_endpoint != ""):
            sample_endpoint = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_endpoint)["SecretString"]
        if (parsed_commands.sample_secret_certificate != ""):
            sample_certificate = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_certificate)
            with open(tmp_certificate_file_path, "w") as file:
                # lgtm [py/clear-text-storage-sensitive-data]
                file.write(sample_certificate["SecretString"])
        if (parsed_commands.sample_secret_private_key != ""):
            sample_private_key = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_private_key)
            with open(tmp_private_key_path, "w") as file:
                # lgtm [py/clear-text-storage-sensitive-data]
                file.write(sample_private_key["SecretString"])
        if (parsed_commands.sample_secret_custom_authorizer_name != ""):
            sample_custom_authorizer_name = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_custom_authorizer_name)["SecretString"]
        if (parsed_commands.sample_secret_custom_authorizer_password != ""):
            sample_custom_authorizer_password = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_custom_authorizer_password)["SecretString"]

    except Exception:
        sys.exit("ERROR: Could not get secrets to launch sample!")

    if (parsed_commands.sample_run_softhsm != ""):
        print ("Setting up private key via SoftHSM")
        subprocess.run("softhsm2-util --init-token --free --label my-token --pin 0000 --so-pin 0000", shell=True)
        subprocess.run(f"softhsm2-util --import {tmp_private_key_path} --token my-token --label my-key --id BEEFCAFE --pin 0000", shell=True)
        print ("Finished setting up private key in SoftHSM")

    print("Launching sample...")
    exit_code = launch_sample(parsed_commands, sample_endpoint, sample_certificate,
                              sample_private_key, sample_custom_authorizer_name, sample_custom_authorizer_password)

    print("Deleting files...")
    if (sample_certificate != ""):
        os.remove(tmp_certificate_file_path)
    if (sample_private_key != ""):
        os.remove(tmp_private_key_path)

    if (exit_code == 0):
        print("SUCCESS: Finished running sample! Exiting with success")
    else:
        print("ERROR: Sample did not return success! Exit code " + str(exit_code))
    return exit_code


def launch_sample(parsed_commands, sample_endpoint, sample_certificate, sample_private_key, sample_custom_authorizer_name, sample_custom_authorizer_password):
    global tmp_certificate_file_path
    global tmp_private_key_path
    exit_code = 0

    print("Processing arguments...")
    launch_arguments = []
    launch_arguments.append("--endpoint")
    launch_arguments.append(sample_endpoint)
    if (sample_certificate != ""):
        launch_arguments.append("--cert")
        launch_arguments.append(tmp_certificate_file_path)
    if (sample_private_key != "" and parsed_commands.sample_run_softhsm == ""):
        launch_arguments.append("--key")
        launch_arguments.append(tmp_private_key_path)
    if (sample_custom_authorizer_name != ""):
        launch_arguments.append("--custom_auth_authorizer_name")
        launch_arguments.append(sample_custom_authorizer_name)
    if (sample_custom_authorizer_password != ""):
        launch_arguments.append("--custom_auth_password")
        launch_arguments.append(sample_custom_authorizer_password)
    if (parsed_commands.sample_arguments != ""):
        sample_arguments_split = parsed_commands.sample_arguments.split(" ")
        for arg in sample_arguments_split:
            launch_arguments.append(arg)

    print("Launching sample...")
    # Based on the programming language, we have to run it a different way
    if (parsed_commands.language == "Java"):
        arguments_as_string = ""
        for i in range(0, len(launch_arguments)):
            arguments_as_string += str(launch_arguments[i])
            if (i+1 < len(launch_arguments)):
                arguments_as_string += " "
        arguments = ["mvn", "compile", "exec:java"]
        arguments.append("-pl")
        arguments.append(parsed_commands.sample_file)
        arguments.append("-Dexec.mainClass=" +
                         parsed_commands.sample_main_class)
        arguments.append("-Daws.crt.ci=True")

        # We have to do this as a string, unfortunately, due to how -Dexec.args= works...
        argument_string = subprocess.list2cmdline(
            arguments) + " -Dexec.args=\"" + arguments_as_string + "\""
        sample_return = subprocess.run(argument_string, shell=True)
        exit_code = sample_return.returncode

    elif (parsed_commands.language == "CPP"):
        sample_return = subprocess.run(
            args=launch_arguments, executable=parsed_commands.sample_file)
        exit_code = sample_return.returncode

    elif (parsed_commands.language == "Python"):
        launch_arguments.append("--is_ci")
        launch_arguments.append("True")

        sample_return = subprocess.run(
            args=[sys.executable, parsed_commands.sample_file] + launch_arguments)
        exit_code = sample_return.returncode

    elif (parsed_commands.language == "Javascript"):
        os.chdir(parsed_commands.sample_file)
        sample_return_one = subprocess.run(args=["npm", "install"])
        if (sample_return_one.returncode != 0):
            exit_code = sample_return_one.returncode
        else:
            arguments = ["node", "dist/index.js"]
            sample_return_two = subprocess.run(
                args=arguments + launch_arguments)
            exit_code = sample_return_two.returncode

    else:
        print("ERROR - unknown programming language! Supported programming languages are 'Java', 'CPP', 'Python', and 'Javascript'")
        return -1

    # finish!
    return exit_code


def main():
    argument_parser = argparse.ArgumentParser(
        description="Run Sample in CI")
    argument_parser.add_argument("--language", metavar="<CPP, Java, Python, or Javascript>", required=True,
                                 help="The name of the programming language. Used to determine how to launch the sample")
    argument_parser.add_argument("--sample_file",
                                 metavar="<CPP=C:\\repository\\PubSub.exe, Java=samples/BasicPubSub, Python=PubSub.py, Javascript=C:\\samples\\node\\pub_sub>",
                                 required=True, default="", help="Sample to launch. Format varies based on programming language")
    argument_parser.add_argument("--sample_region", metavar="<Name of region>",
                                 required=True, default="us-east-1", help="The name of the region to use for accessing secrets")
    argument_parser.add_argument("--sample_secret_endpoint", metavar="<Name of endpoint secret>",
                                 required=False, default="", help="The name of the secret containing the endpoint")
    argument_parser.add_argument("--sample_secret_certificate", metavar="<Name of certificate secret>", required=False,
                                 default="", help="The name of the secret containing the certificate PEM file")
    argument_parser.add_argument("--sample_secret_private_key", metavar="<Name of private key secret>", required=False,
                                 default="", help="The name of the secret containing the private key PEM file")
    argument_parser.add_argument("--sample_secret_custom_authorizer_name", metavar="<Name of custom authorizer name secret>", required=False,
                                 default="", help="The name of the secret containing the custom authorizer name")
    argument_parser.add_argument("--sample_secret_custom_authorizer_password", metavar="<Name of custom authorizer password secret>", required=False,
                                 default="", help="The name of the secret containing the custom authorizer password")
    argument_parser.add_argument("--sample_run_softhsm", metavar="<Set to 'True' to run SoftHSM>", required=False,
                                 default="", help="Runs SoftHSM on the private key passed, storing it, rather than passing it directly to the sample. Used for PKCS11 sample")
    argument_parser.add_argument("--sample_arguments", metavar="<Arguments here in single string!>",
                                 required=False, default="",
                                 help="Arguments to pass to sample. In Java, these arguments will be in a double quote (\") string")
    argument_parser.add_argument("--sample_main_class", metavar="<pubsub.PubSub - Java ONLY>",
                                 required=False, default="", help="Java only: The main class to run")

    parsed_commands = argument_parser.parse_args()

    print("Starting to launch sample...")
    sample_result = getSecretsAndLaunch(parsed_commands)
    sys.exit(sample_result)


if __name__ == "__main__":
    main()
