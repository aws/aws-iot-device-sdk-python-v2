#!/bin/bash

set -e

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "unit-test/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Mqtt Direct test"
python3 pubsub.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem

echo "Websocket test"
python3 pubsub.py --endpoint $ENDPOINT --use-websocket --signing-region us-east-1

popd
