#!/bin/bash

set -e
set -o pipefail

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "ci/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "MQTT5 PubSub test"
python3 mqtt5_pubsub.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem --is_ci "true"

popd
