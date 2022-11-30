#!/bin/bash

set -e
set -o pipefail

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "ci/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Basic Connect test"
python3 basic_connect.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem

echo "Websocket Connect test"
python3 websocket_connect.py --endpoint $ENDPOINT --signing_region us-east-1

popd
