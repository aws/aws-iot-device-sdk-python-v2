#!/bin/bash

# Get the S3 URL containing all of the MQTT5 testing environment variables passed in to the bash script
testing_env_bucket=$1
region=$2

# Make sure we have something:
if [ "${testing_env_bucket}" != "" ] && [ "${region}" != "" ]; then
    echo "S3 bucket for environment variables found and region"
else
    echo "Could not get S3 bucket for environment variables and/or region."
    echo "You need to run this script and pass the S3 URL of the file containing"
    echo "all of the environment variables to set, as well as the secrets for certificates and private keys"
    echo ""
    echo "Example: test_setup.sh s3://<bucket>/<file> <region>"
    echo ""
    return 1
fi

# Get the file from S3
aws s3 cp ${testing_env_bucket} ${PWD}/environment_files.txt
testing_env_file=$( cat environment_files.txt )
# Make sure we have data of some form
if [ "${testing_env_file}" != "" ]; then
    echo "Environment variables secret found"
else
    echo "Could not get environment variables from secrets!"
    return 1
fi

# Make all the variables in mqtt5_environment_variables.txt exported
# so we can run MQTT5 tests
export $(grep -v '^#' environment_files.txt | xargs)

valid_setup=true

# CRT/non-builder certificate and key processing
# Get the certificate and key secrets (dumps straight to a file)
crt_cert_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_MQTT5_CERTIFICATE_FILE_SECRET}" --query "SecretString" --region ${region} | cut -f2 -d\") && echo "$crt_cert_file" > ${PWD}/crt_certificate.pem
crt_key_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_MQTT5_KEY_FILE_SECRET}" --query "SecretString" --region ${region} | cut -f2 -d\") && echo "$crt_key_file" > ${PWD}/crt_privatekey.pem

# IoT/Builder certificate and key processing
# Get the certificate and key secrets (dumps straight to a file)
iot_cert_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH_SECRET}" --region ${region} --query "SecretString" | cut -f2 -d":" | cut -f2 -d\") && echo -e "$iot_cert_file" > ${PWD}/iot_certificate.pem
iot_key_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_MQTT5_IOT_KEY_PATH_SECRET}" --region ${region} --query "SecretString" | cut -f2 -d":" | cut -f2 -d\") && echo -e "$iot_key_file" > ${PWD}/iot_privatekey.pem

provision_cert_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_IOT_CORE_PROVISIONING_CERTIFICATE_PATH_SECRET}" --region ${region} --query "SecretString" | cut -f2 -d":" | cut -f2 -d\") && echo -e "$provision_cert_file" > ${PWD}/provision_certificate.pem
provision_key_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_IOT_CORE_PROVISIONING_KEY_PATH_SECRET}" --region ${region} --query "SecretString" | cut -f2 -d":" | cut -f2 -d\") && echo -e "$provision_key_file" > ${PWD}/provision_key.pem
provision_csr_file=$(aws secretsmanager get-secret-value --secret-id "${AWS_TEST_IOT_CORE_PROVISIONING_CSR_PATH_SECRET}" --region ${region} --query "SecretString" | cut -f2 -d":" | cut -f2 -d\") && echo -e "$provision_csr_file" > ${PWD}/provision_csr.pem

# Do the certificate and key files have data? If not, then abort!
if [ "${crt_cert_file}" = "" ] || [ "${crt_key_file}" = "" ] || [ "${iot_cert_file}" = "" ] || [ "${iot_key_file}" = "" ]; then
    valid_setup=false
fi

if [ "${provision_cert_file}" = "" ] || [ "${provision_key_file}" = "" ] || [ "${provision_csr_file}" = "" ]; then
    valid_setup=false
fi

if [ "$valid_setup" = false ]; then
    # Clean up...
    unset $(grep -v '^#' environment_files.txt | xargs | cut -d "=" -f 1)
    rm "${PWD}/environment_files.txt"
    rm "${PWD}/crt_certificate.pem"
    rm "${PWD}/crt_privatekey.pem"
    rm "${PWD}/iot_certificate.pem"
    rm "${PWD}/iot_privatekey.pem"
    rm "${PWD}/provision_certificate.pem"
    rm "${PWD}/provision_key.pem"
    rm "${PWD}/provision_csr.pem"

    return 1
fi

# Set the certificate and key paths (absolute paths for best compatbility)
export AWS_TEST_MQTT5_CERTIFICATE_FILE="${PWD}/crt_certificate.pem"
export AWS_TEST_MQTT5_KEY_FILE="${PWD}/crt_privatekey.pem"

# Set IoT certificate and key paths
export AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH="${PWD}/iot_certificate.pem"
export AWS_TEST_MQTT5_IOT_KEY_PATH="${PWD}/iot_privatekey.pem"

# Set provisioning cert and key paths
export AWS_TEST_IOT_CORE_PROVISIONING_CERTIFICATE_PATH="${PWD}/provision_certificate.pem"
export AWS_TEST_IOT_CORE_PROVISIONING_KEY_PATH="${PWD}/provision_key.pem"
export AWS_TEST_IOT_CORE_PROVISIONING_CSR_PATH="${PWD}/provision_csr.pem"

# Everything is set
echo "Success: Environment variables set!"
