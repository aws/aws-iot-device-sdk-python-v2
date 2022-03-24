#!/bin/bash

set -e

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "unit-test/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "PubSub test"
python3 pubsub.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem

popd
