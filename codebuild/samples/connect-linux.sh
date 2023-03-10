#!/bin/bash

set -e
set -o pipefail

env

pushd $CODEBUILD_SRC_DIR/samples/basic_connect

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "ci/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Basic Connect test"
python3 basic_connect.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem

popd
pushd $CODEBUILD_SRC_DIR/samples/websocket_connect

echo "Websocket Connect test"
python3 websocket_connect.py --endpoint $ENDPOINT --signing_region us-east-1

popd
