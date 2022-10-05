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

current_folder = os.path.dirname(pathlib.Path(__file__).resolve())
if sys.platform == "win32" or sys.platform == "cygwin":
    current_folder += "\\"
else:
    current_folder += "/"
tmp_certificate_file_path = str(current_folder) + "tmp_certificate.pem"
tmp_private_key_path = str(current_folder) + "tmp_privatekey.pem.key"
tmp_pfx_file_path = str(current_folder) + "tmp_pfx_certificate.pfx"
tmp_pfx_certificate_path = ""
tmp_pfx_certificate_store_location = "CurrentUser\\My"
tmp_pfx_password = "" # Setting a password causes issues, but an empty string is valid so we use that


def get_secrets_and_launch(parsed_commands):
    global tmp_certificate_file_path
    global tmp_private_key_path
    global tmp_pfx_file_path
    global tmp_pfx_certificate_path
    exit_code = 0
    sample_endpoint = ""
    sample_certificate = ""
    sample_private_key = ""
    sample_custom_authorizer_name = ""
    sample_custom_authorizer_password = ""

    print("Attempting to get credentials from secrets using Boto3...")
    secrets_client = boto3.client(
        "secretsmanager", region_name=parsed_commands.sample_region)
    try:
        if (parsed_commands.sample_secret_endpoint != ""):
            sample_endpoint = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_endpoint)["SecretString"]
        if (parsed_commands.sample_secret_certificate != ""):
            secret_data = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_certificate)
            with open(tmp_certificate_file_path, "w") as file:
                # lgtm [py/clear-text-storage-sensitive-data]
                file.write(secret_data["SecretString"])
            sample_certificate = tmp_certificate_file_path
        if (parsed_commands.sample_secret_private_key != ""):
            secret_data = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_private_key)
            with open(tmp_private_key_path, "w") as file:
                # lgtm [py/clear-text-storage-sensitive-data]
                file.write(secret_data["SecretString"])
            sample_private_key = tmp_private_key_path
        if (parsed_commands.sample_secret_custom_authorizer_name != ""):
            sample_custom_authorizer_name = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_custom_authorizer_name)["SecretString"]
        if (parsed_commands.sample_secret_custom_authorizer_password != ""):
            sample_custom_authorizer_password = secrets_client.get_secret_value(
                SecretId=parsed_commands.sample_secret_custom_authorizer_password)["SecretString"]

    except Exception:
        sys.exit("ERROR: Could not get secrets to launch sample!")

    extra_step_return = 0
    if (parsed_commands.sample_run_softhsm != ""):
        extra_step_return = make_softhsm_key()
        sample_private_key = "" # Do not use the private key
    if (parsed_commands.sample_run_certutil != ""):
        extra_step_return = make_windows_pfx_file()
        sample_private_key = "" # Do not use the private key
        sample_certificate = tmp_pfx_certificate_path # use the Windows certificate path

    exit_code = extra_step_return
    if (extra_step_return == 0):
        print("Launching sample...")
        exit_code = launch_sample(parsed_commands, sample_endpoint, sample_certificate,
                                sample_private_key, sample_custom_authorizer_name, sample_custom_authorizer_password)

        if (exit_code == 0):
            print("SUCCESS: Finished running sample! Exiting with success")
        else:
            print("ERROR: Sample did not return success! Exit code " + str(exit_code))
    else:
        print ("ERROR: Could not run extra step (SoftHSM, CertUtil, etc)")

    print("Deleting files...")
    if (os.path.isfile(tmp_certificate_file_path)):
        os.remove(tmp_certificate_file_path)
    if (os.path.isfile(tmp_private_key_path)):
        os.remove(tmp_private_key_path)
    if (os.path.isfile(tmp_pfx_file_path)):
        os.remove(tmp_pfx_file_path)

    return exit_code


def make_softhsm_key():
    print ("Setting up private key via SoftHSM")
    softhsm_run = subprocess.run("softhsm2-util --init-token --free --label my-token --pin 0000 --so-pin 0000", shell=True)
    if (softhsm_run.returncode != 0):
        print ("ERROR: SoftHSM could not initialize a new token")
        return softhsm_run.returncode
    softhsm_run = subprocess.run(f"softhsm2-util --import {tmp_private_key_path} --token my-token --label my-key --id BEEFCAFE --pin 0000", shell=True)
    if (softhsm_run.returncode != 0):
        print ("ERROR: SoftHSM could not import token")
    print ("Finished setting up private key in SoftHSM")
    return 0


def make_windows_pfx_file():
    global tmp_certificate_file_path
    global tmp_private_key_path
    global tmp_pfx_file_path
    global tmp_pfx_certificate_path

    if sys.platform == "win32" or sys.platform == "cygwin":
        if os.path.isfile(tmp_certificate_file_path) != True:
            print (tmp_certificate_file_path)
            print("ERROR: Certificate file not found!")
            return 1
        if os.path.isfile(tmp_private_key_path) != True:
            print("ERROR: Private key file not found!")
            return 1

        # Delete old PFX file if it exists
        if os.path.isfile(tmp_pfx_file_path):
            os.remove(tmp_pfx_file_path)

        # Make a key copy
        copy_path = os.path.splitext(tmp_certificate_file_path)
        with open(copy_path[0] + ".key", 'w') as file:
            key_file = open(tmp_private_key_path)
            file.write(key_file.read())
            key_file.close()

        # Make a PFX file
        certutil_error_occurred = False
        arguments = ["certutil",  "-mergePFX", tmp_certificate_file_path, tmp_pfx_file_path]
        certutil_run = subprocess.run(args=arguments, shell=True, input=f"{tmp_pfx_password}\n{tmp_pfx_password}", encoding='ascii')
        if (certutil_run.returncode != 0):
            print ("ERROR: Could not make PFX file")
            certutil_error_occurred = True
            return 1
        else:
            print ("PFX file created successfully")

        # Remove the temporary key copy
        if os.path.isfile(copy_path[0] + ".key"):
            os.remove(copy_path[0] + ".key")
        if (certutil_error_occurred == True):
            return 1

        # Import the PFX into the Windows Certificate Store
        # (Passing '$mypwd' is required even though it is empty and our certificate has no password. It fails CI otherwise)
        import_pfx_arguments = ["powershell.exe", "Import-PfxCertificate", "-FilePath", tmp_pfx_file_path, "-CertStoreLocation", "Cert:\\" + tmp_pfx_certificate_store_location, "-Password", "$mypwd"]
        import_pfx_run = subprocess.run(args=import_pfx_arguments, shell=True, stdout=subprocess.PIPE)
        if (import_pfx_run.returncode != 0):
            print ("ERROR: Could not import PFX certificate into Windows store!")
            return 1
        else:
            print ("Certificate imported to Windows Certificate Store successfully")

        # Get the certificate thumbprint from the output:
        import_pfx_output = str(import_pfx_run.stdout)
        # We know the Thumbprint will always be 40 characters long, so we can find it using that
        # TODO: Extract this using a better method
        thumbprint = ""
        current_str = ""
        # The input comes as a string with some special characters still included, so we need to remove them!
        import_pfx_output = import_pfx_output.replace("\\r", " ")
        import_pfx_output = import_pfx_output.replace("\\n", "\n")
        for i in range(0, len(import_pfx_output)):
            if (import_pfx_output[i] == " " or import_pfx_output[i] == "\n"):
                if (len(current_str) == 40):
                    thumbprint = current_str
                    break
                current_str = ""
            else:
                current_str += import_pfx_output[i]

        # Did we get a thumbprint?
        if (thumbprint == ""):
            print ("ERROR: Could not find certificate thumbprint")
            return 1

        # Construct the certificate path
        tmp_pfx_certificate_path = tmp_pfx_certificate_store_location + "\\" + thumbprint

        # Return success
        print ("PFX certificate created and imported successfully!")
        return 0

    else:
        print("ERROR - Windows PFX file can only be created on a Windows platform!")
        return 1


def launch_sample(parsed_commands, sample_endpoint, sample_certificate, sample_private_key, sample_custom_authorizer_name, sample_custom_authorizer_password):
    global tmp_certificate_file_path
    global tmp_private_key_path
    global tmp_pfx_file_path
    exit_code = 0

    print("Processing arguments...")
    launch_arguments = []
    launch_arguments.append("--endpoint")
    launch_arguments.append(sample_endpoint)

    if (sample_certificate != ""):
        launch_arguments.append("--cert")
        launch_arguments.append(sample_certificate)
    if (sample_private_key != ""):
        launch_arguments.append("--key")
        launch_arguments.append(sample_private_key)
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

        launch_arguments.append("--is_ci")
        launch_arguments.append("true")

        sample_return_one = None
        if sys.platform == "win32" or sys.platform == "cygwin":
            sample_return_one = subprocess.run(args=["npm", "install"], shell=True)
        else:
            sample_return_one = subprocess.run(args=["npm", "install"])

        if (sample_return_one == None or sample_return_one.returncode != 0):
            exit_code = sample_return_one.returncode
        else:
            sample_return_two = None
            arguments = []
            if (parsed_commands.node_cmd == "" or parsed_commands.node_cmd == None):
                arguments = ["node", "dist/index.js"]
            else:
                arguments = parsed_commands.node_cmd.split(" ")

            if sys.platform == "win32" or sys.platform == "cygwin":
                sample_return_two = subprocess.run(
                    args=arguments + launch_arguments, shell=True)
            else:
                sample_return_two = subprocess.run(
                    args=arguments + launch_arguments)

            if (sample_return_two != None):
                exit_code = sample_return_two.returncode
            else:
                exit_code = 1

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
    argument_parser.add_argument("--sample_run_softhsm", metavar="<Set to 'True' to run SoftHSM (Linux ONLY)>", required=False,
                                 default="", help="Runs SoftHSM on the private key passed, storing it, rather than passing it directly to the sample. Used for PKCS11 sample")
    argument_parser.add_argument("--sample_run_certutil", metavar="<Set to 'True' to run Certutil (Windows ONLY)>", required=False,
                                 default="", help="Runs CertUtil on the private key and certificate passed and makes a certificate.pfx file, "
                                 "which is used automatically in the --cert argument. Used for Windows Certificate Connect sample")
    argument_parser.add_argument("--sample_arguments", metavar="<Arguments here in single string!>",
                                 required=False, default="",
                                 help="Arguments to pass to sample. In Java, these arguments will be in a double quote (\") string")
    argument_parser.add_argument("--sample_main_class", metavar="<pubsub.PubSub - Java ONLY>",
                                 required=False, default="", help="Java only: The main class to run")
    argument_parser.add_argument("--node_cmd", metavar="<node index.js - Javascript ONLY>", required=False, default="",
                                 help="Javascript only: Overrides the default 'npm dist/index.js' with whatever you pass. Useful for launching pure Javascript samples")

    parsed_commands = argument_parser.parse_args()

    print("Starting to launch sample...")
    sample_result = get_secrets_and_launch(parsed_commands)
    sys.exit(sample_result)


if __name__ == "__main__":
    main()
