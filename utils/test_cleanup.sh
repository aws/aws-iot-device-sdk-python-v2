#!/bin/bash

echo "Undoing environment variables"
unset $(grep -v '^#' ${PWD}/environment_files.txt | xargs | cut -d "=" -f 1)
unset AWS_TEST_MQTT5_CERTIFICATE_FILE
unset AWS_TEST_MQTT5_KEY_FILE
unset AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH
unset AWS_TEST_MQTT5_IOT_KEY_PATH
unset AWS_TEST_IOT_CORE_PROVISIONING_CERTIFICATE_PATH
unset AWS_TEST_IOT_CORE_PROVISIONING_KEY_PATH
unset AWS_TEST_IOT_CORE_PROVISIONING_CSR_PATH

echo "Cleaning up resources..."
rm "${PWD}/environment_files.txt"
rm "${PWD}/crt_certificate.pem"
rm "${PWD}/crt_privatekey.pem"
rm "${PWD}/iot_certificate.pem"
rm "${PWD}/iot_privatekey.pem"
rm "${PWD}/provision_certificate.pem"
rm "${PWD}/provision_key.pem"
rm "${PWD}/provision_csr.pem"

echo "Success!"
return 0
