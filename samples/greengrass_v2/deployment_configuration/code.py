#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import time
import os
import http.server
import socketserver

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2

client = GreengrassCoreIPCClientV2()
thing_name = os.environ["AWS_IOT_THING_NAME"]


def main():
    # https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-component-configuration.html
    config = client.get_configuration().value

    print("This component was deployed with the following configuration:", config)

    # example use case that takes component configuration as arguments for a webserver
    host = config["Webserver"]["Host"]
    port = config["Webserver"]["Port"]
    directory = config["Webserver"]["Directory"]

    os.chdir(directory)

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((host, port), Handler) as httpd:
        print(f"serving at {host}:{port} ...")
        httpd.serve_forever()


if __name__ == "__main__":
    # Once we enter here, we know:
    #   * all dependencies are available (imports succeeded)
    #   * IPC Client created
    #   * AWS_IOT_THING_NAME environment variable is available
    # This should be sufficient to consider this component `running` and the deployment will be completed.
    # If any of these failed, the component will be `broken`, and the deployment might roll-back or report the error.
    # Once the component is `running`, we need to try as hard as possible to keep it alive and running.
    while True:
        try:
            main()
        except Exception as e:
            print("ERROR", e)
        time.sleep(5)
