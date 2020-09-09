# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

"""

A simply utility script to parse out certificates and keys from some IoT operations.

For example, you may be doing fleet provisioning and want to have a simple way of setting up the results from create-provisioning-claim
into usable pem files that you can make IoT connections with.

Example usage:

aws iot create-provisioning-claim --template-name <TemplateName> | python3 parse_cert_set_result.py --path <PathToOutputtedCerts> --filename <Filename>

"""

import argparse
import json
import os
import re
import sys

parser = argparse.ArgumentParser(description="Utility script to generate valid .cert.pem, .private.key, .public.key files from the JSON response of CreateProvisioningClaim, CreateCertificateFromCsr")
parser.add_argument('--path', required=True, help="Path to extract the certificate set files to.  Created if does not exist")
parser.add_argument('--filename', required=True, help="Filename (prefix) to use for the generated files")

if __name__ == '__main__':
    # Process input args
    args = parser.parse_args()

    path = args.path
    filename = args.filename

    if not os.path.exists(path):
        os.makedirs(path)

    body = json.load(sys.stdin)

    raw_pem = body['certificatePem']
    if raw_pem:
        pem = re.sub("\\n", "\n", raw_pem)
        pem_filename = os.path.join(path, filename + ".cert.pem")
        with open(pem_filename, 'w') as file:
            file.write(pem)

    try:
        raw_pub_key = body['keyPair']['PublicKey']
        if raw_pub_key:
            pub_key = re.sub("\\n", "\n", raw_pub_key)
            pub_key_filename = os.path.join(path, filename + ".public.key")
            with open(pub_key_filename, 'w') as file:
                file.write(pub_key)

        raw_private_key = body['keyPair']['PrivateKey']
        if raw_private_key:
            private_key = re.sub("\\n", "\n", raw_private_key)
            private_key_filename = os.path.join(path, filename + ".private.key")
            with open(private_key_filename, 'w') as file:
                file.write(private_key)
    except KeyError:
        pass

    print("Success!")






