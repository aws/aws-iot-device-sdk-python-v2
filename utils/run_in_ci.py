# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# Built-in
import argparse
import os
import subprocess
import pathlib
import sys
import json
# Needs to be installed via pip
import boto3

current_folder = os.path.dirname(pathlib.Path(__file__).resolve())
if sys.platform == "win32" or sys.platform == "cygwin":
    current_folder += "\\"
else:
    current_folder += "/"

config_json = None
config_json_arguments_list = []

pfx_certificate_store_location = "CurrentUser\\My"
pfx_password = "" # Setting a password causes issues, but an empty string is valid so we use that

def setup_json_arguments_list(file, input_uuid=None):
    global config_json
    global config_json_arguments_list

    print("Attempting to get credentials from secrets using Boto3...")
    secrets_client = boto3.client("secretsmanager", region_name=config_json['runnable_region'])
    print("Processing arguments...")

    for argument in config_json['arguments']:
        # Add the name of the argument
        if( 'name' in argument):
            config_json_arguments_list.append(argument['name'])

        # Based on the data present, we need to process and add the data differently
        try:

            # Is there a secret? If so, decode it!
            if 'secret' in argument:
                secret_data = secrets_client.get_secret_value(SecretId=argument['secret'])["SecretString"]

                # Is this supposed to be stored in a file?
                if 'filename' in argument:
                    with open(str(current_folder) + argument['filename'], "w") as file:
                        # lgtm [py/clear-text-storage-sensitive-data]
                        file.write(secret_data)
                    config_json_arguments_list.append(str(current_folder) + argument['filename'])
                else:
                    config_json_arguments_list.append(secret_data)

                if 'pkcs11_key' in argument:
                    pkcs11_result = make_softhsm_key(str(current_folder) + argument['filename'])
                    if (pkcs11_result != 0):
                        print ("ERROR with PKCS11!")
                        return pkcs11_result

            # Windows 10 certificate store data?
            elif 'windows_cert_certificate' in argument and 'windows_cert_certificate_path' in argument \
                and 'windows_cert_key' in argument and 'windows_cert_key_path' in argument != None \
                and 'windows_cert_pfx_key_path' in argument != None:

                windows_cert_data = secrets_client.get_secret_value(SecretId=argument['windows_cert_certificate'])["SecretString"]
                with open(str(current_folder) + argument['windows_cert_certificate_path'], "w") as file:
                    # lgtm [py/clear-text-storage-sensitive-data]
                    file.write(windows_cert_data)
                windows_key_data = secrets_client.get_secret_value(SecretId=argument['windows_cert_key'])["SecretString"]
                with open(str(current_folder) + argument['windows_cert_key_path'], "w") as file:
                    # lgtm [py/clear-text-storage-sensitive-data]
                    file.write(windows_key_data)

                certificate_path = make_windows_pfx_file(
                    str(current_folder) + argument['windows_cert_certificate_path'],
                    str(current_folder) + argument['windows_cert_key_path'],
                    str(current_folder) + argument['windows_cert_pfx_key_path'])
                config_json_arguments_list.append(certificate_path)

            # Raw data? just add it directly!
            elif 'data' in argument:
                tmp_value = argument['data']
                if isinstance(tmp_value, str) and input_uuid is not None:
                    if ("$INPUT_UUID" in tmp_value):
                        tmp_value = tmp_value.replace("$INPUT_UUID", input_uuid)
                if (tmp_value != None and tmp_value != ""):
                    config_json_arguments_list.append(tmp_value)

            # None of the above? Just print an error
            else:
                print("ERROR - unknown or missing argument value!")

        except Exception as e:
            print(f"Something went wrong processing {argument['name']}: {e}!")
            return -1
    return 0

def make_softhsm_key(private_key_path):
    print ("Setting up private key via SoftHSM")
    softhsm_run = subprocess.run("softhsm2-util --init-token --free --label my-token --pin 0000 --so-pin 0000", shell=True)
    if (softhsm_run.returncode != 0):
        print ("ERROR: SoftHSM could not initialize a new token")
        return softhsm_run.returncode
    softhsm_run = subprocess.run(f"softhsm2-util --import {private_key_path} --token my-token --label my-key --id BEEFCAFE --pin 0000", shell=True)
    if (softhsm_run.returncode != 0):
        print ("ERROR: SoftHSM could not import token")
    print ("Finished setting up private key in SoftHSM")
    return 0


def make_windows_pfx_file(certificate_file_path, private_key_path, pfx_file_path):
    global pfx_certificate_store_location
    global pfx_password

    if sys.platform == "win32" or sys.platform == "cygwin":
        if os.path.isfile(certificate_file_path) != True:
            print (certificate_file_path)
            print("ERROR: Certificate file not found!")
            return 1
        if os.path.isfile(private_key_path) != True:
            print("ERROR: Private key file not found!")
            return 1

        # Delete old PFX file if it exists
        if os.path.isfile(pfx_file_path):
            os.remove(pfx_file_path)

        # Make a key copy
        copy_path = os.path.splitext(certificate_file_path)
        with open(copy_path[0] + ".key", 'w') as file:
            key_file = open(private_key_path)
            file.write(key_file.read())
            key_file.close()

        # Make a PFX file
        arguments = ["certutil",  "-mergePFX", certificate_file_path, pfx_file_path]
        certutil_run = subprocess.run(args=arguments, shell=True, input=f"{pfx_password}\n{pfx_password}", encoding='ascii')
        if (certutil_run.returncode != 0):
            print ("ERROR: Could not make PFX file")
            return 1
        else:
            print ("PFX file created successfully")

        # Remove the temporary key copy
        if os.path.isfile(copy_path[0] + ".key"):
            os.remove(copy_path[0] + ".key")

        # Import the PFX into the Windows Certificate Store
        # (Passing '$mypwd' is required even though it is empty and our certificate has no password. It fails CI otherwise)
        import_pfx_arguments = [
            "powershell.exe",
            # Powershell 7.3 introduced an issue where launching powershell from cmd would not set PSModulePath correctly.
            # As a workaround, we set `PSModulePath` to empty so powershell would automatically reset the PSModulePath to default.
            # More details: https://github.com/PowerShell/PowerShell/issues/18530
            "$env:PSModulePath = '';",
            "Import-PfxCertificate",
            "-FilePath", pfx_file_path,
            "-CertStoreLocation",
            "Cert:\\" + pfx_certificate_store_location,
            "-Password",
            "$mypwd"]
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
        print ("PFX certificate created and imported successfully!")
        return pfx_certificate_store_location + "\\" + thumbprint

    else:
        print("ERROR - Windows PFX file can only be created on a Windows platform!")
        return 1

def setup_runnable(file, input_uuid=None):
    global config_json

    file_absolute = pathlib.Path(file).resolve()
    json_file_data = ""
    with open(file_absolute, "r") as json_file:
        json_file_data = json_file.read()

    # Load the JSON data
    config_json = json.loads(json_file_data)

    # Make sure required parameters are all there
    if not 'language' in config_json or not 'runnable_file' in config_json \
       or not 'runnable_region' in config_json or not 'runnable_main_class' in config_json:
        return -1

    # Preprocess runnable arguments (get secret data, etc)
    setup_result = setup_json_arguments_list(file, input_uuid)
    if setup_result != 0:
        return setup_result

    print("JSON config file loaded!")
    return 0


def cleanup_runnable():
    global config_json
    global config_json_arguments_list

    for argument in config_json['arguments']:
        if( 'name' in argument):
            config_json_arguments_list.append(argument['name'])

        # Based on the data present, we need to process and add the data differently
        try:
            # Is there a file? If so, clean it!
            if 'filename' in argument:
                if (os.path.isfile(str(current_folder) + argument['filename'])):
                    os.remove(str(current_folder) + argument['filename'])

            # Windows 10 certificate store data?
            if 'windows_cert_certificate' in argument and 'windows_cert_certificate_path' in argument \
                    and 'windows_cert_key' in argument and 'windows_cert_key_path' in argument \
                    and 'windows_cert_pfx_key_path' in argument:

                if (os.path.isfile(str(current_folder) + argument['windows_cert_certificate_path'])):
                    os.remove(str(current_folder) + argument['windows_cert_certificate_path'])
                if (os.path.isfile(str(current_folder) + argument['windows_cert_key_path'])):
                    os.remove(str(current_folder) + argument['windows_cert_key_path'])
                if (os.path.isfile(str(current_folder) + argument['windows_cert_pfx_key_path'])):
                    os.remove(str(current_folder) + argument['windows_cert_pfx_key_path'])

        except Exception as e:
            print(f"Something went wrong cleaning {argument['name']}!")
            return -1


def launch_runnable(runnable_dir):
    global config_json
    global config_json_arguments_list

    if (config_json == None):
        print("No configuration JSON file data found!")
        return -1

    # Prepare data for runnable's STDIN
    subprocess_stdin = None
    if "stdin_file" in config_json:
        stdin_file = os.path.join(runnable_dir, config_json['stdin_file'])
        with open(stdin_file, "rb") as file:
            subprocess_stdin = file.read()

    exit_code = 0

    runnable_timeout = None
    if ('timeout' in config_json):
        runnable_timeout = config_json['timeout']

    print("Launching runnable...")

    try:
        # Java
        if (config_json['language'] == "Java"):
            # Flatten arguments down into a single string
            arguments_as_string = ""
            for i in range(0, len(config_json_arguments_list)):
                arguments_as_string += str(config_json_arguments_list[i])
                if (i+1 < len(config_json_arguments_list)):
                    arguments_as_string += " "

            arguments = ["mvn", "compile", "exec:java"]
            arguments.append("-pl")
            arguments.append(config_json['runnable_file'])
            arguments.append("-Dexec.mainClass=" + config_json['runnable_main_class'])
            arguments.append("-Daws.crt.ci=True")

            # We have to do this as a string, unfortunately, due to how -Dexec.args= works...
            argument_string = subprocess.list2cmdline(arguments) + " -Dexec.args=\"" + arguments_as_string + "\""
            print(f"Running cmd: {argument_string}")
            runnable_return = subprocess.run(argument_string, input=subprocess_stdin, timeout=runnable_timeout, shell=True)
            exit_code = runnable_return.returncode

        elif (config_json['language'] == "Java JAR"):
            # Flatten arguments down into a single string
            arguments_as_string = ""
            for i in range(0, len(config_json_arguments_list)):
                arguments_as_string += str(config_json_arguments_list[i])
                if (i+1 < len(config_json_arguments_list)):
                    arguments_as_string += " "

            runnable_file = os.path.join(runnable_dir, config_json['runnable_file'])

            arguments = ["java"]
            arguments.append("-Daws.crt.ci=True")
            arguments.append("-jar")
            arguments.append(runnable_file)

            argument_string = subprocess.list2cmdline(arguments) + " " + arguments_as_string
            print(f"Running cmd: {argument_string}")
            runnable_return = subprocess.run(argument_string, input=subprocess_stdin, timeout=runnable_timeout, shell=True)
            exit_code = runnable_return.returncode

        # C++
        elif (config_json['language'] == "CPP"):
            runnable_file = os.path.join(runnable_dir, config_json['runnable_file'])
            runnable_return = subprocess.run(args=config_json_arguments_list, input=subprocess_stdin, timeout=runnable_timeout, executable=runnable_file)
            exit_code = runnable_return.returncode

        elif (config_json['language'] == "Python"):
            runnable_file = os.path.join(runnable_dir, config_json['runnable_file'])
            runnable_return = subprocess.run(
                args=[sys.executable, runnable_file] + config_json_arguments_list, input=subprocess_stdin, timeout=runnable_timeout)
            exit_code = runnable_return.returncode

        elif (config_json['language'] == "Javascript"):
            os.chdir(config_json['runnable_file'])

            config_json_arguments_list.append("--is_ci")
            config_json_arguments_list.append("true")

            runnable_return_one = None
            if not 'skip_install' in config_json:
                if sys.platform == "win32" or sys.platform == "cygwin":
                    runnable_return_one = subprocess.run(args=["npm", "install"], shell=True, timeout=runnable_timeout)
                else:
                    runnable_return_one = subprocess.run(args=["npm", "install"], timeout=runnable_timeout)

            if not 'skip_install' in config_json and (runnable_return_one == None or runnable_return_one.returncode != 0):
                exit_code = runnable_return_one.returncode
            else:
                runnable_return_two = None
                arguments = []
                if 'node_cmd' in config_json:
                    arguments = config_json['node_cmd'].split(" ")
                else:
                    arguments = ["node", "dist/index.js"]

                if sys.platform == "win32" or sys.platform == "cygwin":
                    runnable_return_two = subprocess.run(
                        args=arguments + config_json_arguments_list, shell=True, check=True, timeout=runnable_timeout)
                else:
                    runnable_return_two = subprocess.run(
                        args=arguments + config_json_arguments_list, input=subprocess_stdin, timeout=runnable_timeout)

                if (runnable_return_two != None):
                    exit_code = runnable_return_two.returncode
                else:
                    exit_code = 1
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit_code = 1

    cleanup_runnable()
    return exit_code


def setup_and_launch(file, input_uuid=None, runnable_dir=''):
    setup_result = setup_runnable(file, input_uuid)
    if setup_result != 0:
        print("Setting up runnable failed")
        return setup_result

    print("About to launch runnable...")
    return launch_runnable(runnable_dir)


def main():
    argument_parser = argparse.ArgumentParser(
        description="Run runnable in CI")
    argument_parser.add_argument("--file", required=True, help="Configuration file to pull CI data from")
    argument_parser.add_argument("--input_uuid", required=False,
                                 help="UUID data to replace '$INPUT_UUID' with. Only works in Data field")
    argument_parser.add_argument("--runnable_dir", required=False, default='',
                                 help="Directory where runnable_file is located")
    parsed_commands = argument_parser.parse_args()

    file = parsed_commands.file
    input_uuid = parsed_commands.input_uuid
    runnable_dir = parsed_commands.runnable_dir

    print(f"Starting to launch runnable: config {file}; input UUID: {input_uuid}")
    test_result = setup_and_launch(file, input_uuid, runnable_dir)
    sys.exit(test_result)


if __name__ == "__main__":
    main()
