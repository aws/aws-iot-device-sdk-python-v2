#!/bin/bash

set -e
set -o pipefail

pushd $CODEBUILD_SRC_DIR/samples/

ENDPOINT=$(aws secretsmanager get-secret-value --secret-id "ci/endpoint" --query "SecretString" | cut -f2 -d":" | sed -e 's/[\\\"\}]//g')

# from hereon commands are echoed. don't leak secrets
set -x

softhsm2-util --version

# SoftHSM2's default tokendir path might be invalid on this machine
# so set up a conf file that specifies a known good tokendir path
mkdir -p /tmp/tokens
export SOFTHSM2_CONF=/tmp/softhsm2.conf
echo "directories.tokendir = /tmp/tokens" > /tmp/softhsm2.conf

# create token
softhsm2-util --init-token --free --label my-token --pin 0000 --so-pin 0000

# add private key to token (must be in PKCS#8 format)
openssl pkcs8 -topk8 -in /tmp/privatekey.pem -out /tmp/privatekey.p8.pem -nocrypt
softhsm2-util --import /tmp/privatekey.p8.pem --token my-token --label my-key --id BEEFCAFE --pin 0000

# run sample
python3 pkcs11_connect.py --endpoint $ENDPOINT --cert /tmp/certificate.pem --pkcs11_lib /usr/lib/softhsm/libsofthsm2.so --pin 0000 --token_label my-token --key_label my-key

popd
