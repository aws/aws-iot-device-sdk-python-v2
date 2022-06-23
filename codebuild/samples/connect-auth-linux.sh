#!/bin/bash

set -e

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "unit-test/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')
AUTH_NAME=$(aws secretsmanager get-secret-value --secret-id "unit-test/authorizer-name" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')
AUTH_PASSWORD=$(aws secretsmanager get-secret-value --secret-id "unit-test/authorizer-password" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Custom authorizer connect test"
python3 custom_authorizer_connect.py --endpoint $ENDPOINT --custom_auth_authorizer_name $AUTH_NAME --custom_auth_password $AUTH_PASSWORD

popd
