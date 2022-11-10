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
import boto3  # - for launching sample

current_folder = os.path.dirname(pathlib.Path(__file__).resolve())
if sys.platform == "win32" or sys.platform == "cygwin":
    current_folder += "\\"
else:
    current_folder += "/"

config_json = None
config_json_arguments_list = []

pfx_certificate_store_location = "CurrentUser\\My"
pfx_password = "" # Setting a password causes issues, but an empty string is valid so we use that

def setup_json_arguments_list(parsed_commands):
    global config_json
    global config_json_arguments_list

    print("Attempting to get credentials from secrets using Boto3...")
    secrets_client = boto3.client("secretsmanager", region_name=config_json['sample_region'])
    print ("Processing arguments...")

    for argument in config_json['arguments']:
        # Add the name of the argument
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
                if isinstance(tmp_value, str) and 'input_uuid' in parsed_commands:
                    if ("$INPUT_UUID" in tmp_value):
                        tmp_value = tmp_value.replace("$INPUT_UUID", parsed_commands.input_uuid)
                config_json_arguments_list.append(tmp_value)

            # None of the above? Just print an error
            else:
                print ("ERROR - unknown or missing argument value!")

        except Exception as e:
            print (f"Something went wrong processing {argument['name']}!")
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
        import_pfx_arguments = ["powershell.exe", "Import-PfxCertificate", "-FilePath", pfx_file_path, "-CertStoreLocation", "Cert:\\" + pfx_certificate_store_location, "-Password", "$mypwd"]
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

def setup_sample(parsed_commands):
    global config_json

    file_absolute = pathlib.Path(parsed_commands.file).resolve()
    json_file_data = ""
    with open(file_absolute, "r") as json_file:
        json_file_data = json_file.read()

    # Load the JSON data
    config_json = json.loads(json_file_data)

    # Make sure required parameters are all there
    if not 'language' in config_json or not 'sample_file' in config_json \
       or not 'sample_region' in config_json or not 'sample_main_class' in config_json:
        return -1

    # Preprocess sample arguments (get secret data, etc)
    setup_result = setup_json_arguments_list(parsed_commands)
    if setup_result != 0:
        return setup_result

    print ("JSON config file loaded!")
    return 0


def cleanup_sample():
    global config_json
    global config_json_arguments_list

    for argument in config_json['arguments']:
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
            print (f"Something went wrong cleaning {argument['name']}!")
            return -1


def launch_sample():
    global config_json
    global config_json_arguments_list

    if (config_json == None):
        print ("No configuration JSON file data found!")
        return -1

    exit_code = 0

    print("Launching sample...")

    # Java
    if (config_json['language'] == "Java"):

        # Flatten arguments down into a asingle string
        arguments_as_string = ""
        for i in range(0, len(config_json_arguments_list)):
            arguments_as_string += str(config_json_arguments_list[i])
            if (i+1 < len(config_json_arguments_list)):
                arguments_as_string += " "

        arguments = ["mvn", "compile", "exec:java"]
        arguments.append("-pl")
        arguments.append(config_json['sample_file'])
        arguments.append("-Dexec.mainClass=" + config_json['sample_main_class'])
        arguments.append("-Daws.crt.ci=True")

        # We have to do this as a string, unfortunately, due to how -Dexec.args= works...
        argument_string = subprocess.list2cmdline(arguments) + " -Dexec.args=\"" + arguments_as_string + "\""
        sample_return = subprocess.run(argument_string, shell=True)
        exit_code = sample_return.returncode

    # C++
    elif (config_json['language'] == "CPP"):
        sample_return = subprocess.run(
            args=config_json_arguments_list, executable=config_json['sample_file'])
        exit_code = sample_return.returncode

    elif (config_json['language'] == "Python"):
        config_json_arguments_list.append("--is_ci")
        config_json_arguments_list.append("True")

        sample_return = subprocess.run(
            args=[sys.executable, config_json['sample_file']] + config_json_arguments_list)
        exit_code = sample_return.returncode

    elif (config_json['language'] == "Javascript"):
        os.chdir(config_json['sample_file'])

        config_json_arguments_list.append("--is_ci")
        config_json_arguments_list.append("true")

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
            if 'node_cmd' in config_json:
                arguments = config_json['node_cmd'].split(" ")
            else:
                arguments = ["node", "dist/index.js"]

            if sys.platform == "win32" or sys.platform == "cygwin":
                sample_return_two = subprocess.run(
                    args=arguments + config_json_arguments_list, shell=True)
            else:
                sample_return_two = subprocess.run(
                    args=arguments + config_json_arguments_list)

            if (sample_return_two != None):
                exit_code = sample_return_two.returncode
            else:
                exit_code = 1

    cleanup_sample()
    return exit_code

def setup_sample_and_launch(parsed_commands):
    setup_result = setup_sample(parsed_commands)
    if setup_result != 0:
        return setup_result

    print ("About to launch sample...")
    return launch_sample()

def main():
    argument_parser = argparse.ArgumentParser(
        description="Run Sample in CI")
    argument_parser.add_argument("--file", required=True, help="Configuration file to pull CI data from")
    argument_parser.add_argument("--input_uuid", required=False, help="UUID data to replace '$INPUT_UUID' with. Only works in Data field")
    parsed_commands = argument_parser.parse_args()

    print("Starting to launch sample...")
    sample_result = setup_sample_and_launch(parsed_commands)
    sys.exit(sample_result)


if __name__ == "__main__":
    main()
