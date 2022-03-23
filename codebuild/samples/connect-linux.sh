#!/bin/bash

set -e

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "unit-test/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Mqtt Direct test"
python3 basic_connect.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem

echo "Websocket test"
python3 websocket_connect.py --endpoint $ENDPOINT --signing_region us-east-1

popd
