#!/bin/bash

set -e

env

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "ci/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

echo "Shadow test"
python3 shadow.py --endpoint $ENDPOINT --key /tmp/privatekey.pem --cert /tmp/certificate.pem --thing_name CI_CodeBuild_Thing --is_ci true

popd
