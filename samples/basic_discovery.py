# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import time
import json
from awscrt import io, http
from awscrt.mqtt import QoS
from awsiot.greengrass_discovery import DiscoveryClient
from awsiot import mqtt_connection_builder

# from utils.command_line_utils import CommandLineUtils

allowed_actions = ['both', 'publish', 'subscribe']

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
# cmdData = CommandLineUtils.parse_sample_input_basic_discovery()

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

def parse_sample_input():
    parser = argparse.ArgumentParser(
        description="MQTT5 pub/sub sample (mTLS).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--cert", required=True, dest="input_cert",
                        help="Path to the certificate file to use during mTLS connection establishment")
    parser.add_argument("--key", required=True, dest="input_key",
                        help="Path to the private key file to use during mTLS connection establishment")
    parser.add_argument("--ca_file", dest="input_ca", help="Path to optional CA bundle (PEM)")

    # Messaging
    parser.add_argument("--topic", default=f"test/topic/{uuid.uuid4().hex[:8]}", dest="input_topic", help="Topic")
    parser.add_argument("--message", default="Hello World!", dest="input_message", help="Message payload")
    parser.add_argument("--thing_name", required=True, dest="input_thing_name", help="The name assigned to your IoT Thing.")
    parser.add_argument("--region", required=True, dest="input_signing_region", help="The region to connect through.")
    parser.add_argument("--max_pub_ops", type=int, default=10, dest="input_max_pub_ops", 
                        help="The maximum number of publish operations (optional, default='10').")
    parser.add_argument("--print_discover_resp_only", type=bool, default=False, dest="input_print_discovery_resp_only", 
                        help="(optional, default='False').")
    parser.add_argument("--mode", default='both', dest="input_mode", 
                        help=f"The operation mode (optional, default='both').\nModes:{allowed_actions}")

    # Proxy (optional)
    parser.add_argument("--proxy-host", dest="input_proxy_host", help="HTTP proxy host")
    parser.add_argument("--proxy-port", type=int, default=0, dest="input_proxy_port", help="HTTP proxy port")

    # Misc
    parser.add_argument("--client-id", dest="input_clientId",
                        default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}", help="Client ID")

    return parser.parse_args()

args = parse_sample_input()

# --------------------------------- ARGUMENT PARSING END -----------------------------------------

# [--mode <mode>]

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.input_cert, args.input_key)
if (args.input_ca is not None):
    tls_options.override_default_trust_store_from_path(None, args.input_ca)
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()

proxy_options = None
if args.input_proxy_host is not None and args.input_proxy_port != 0:
    proxy_options = http.HttpProxyOptions(args.input_proxy_host, args.input_proxy_port)

print('Performing greengrass discovery...')
discovery_client = DiscoveryClient(
    io.ClientBootstrap.get_or_create_static_default(),
    socket_options,
    tls_context,
    args.input_signing_region, None, proxy_options)
resp_future = discovery_client.discover(args.input_thing_name)
discover_response = resp_future.result()

print("Received a greengrass discovery result! Not showing result for possible data sensitivity.")

if (args.input_print_discovery_resp_only):
    exit(0)


def on_connection_interupted(connection, error, **kwargs):
    print('connection interrupted with error {}'.format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print('connection resumed with return code {}, session present {}'.format(return_code, session_present))


# Try IoT endpoints until we find one that works
def try_iot_endpoints():
    for gg_group in discover_response.gg_groups:
        for gg_core in gg_group.cores:
            for connectivity_info in gg_core.connectivity:
                try:
                    print(
                        f"Trying core {gg_core.thing_arn} at host {connectivity_info.host_address} port {connectivity_info.port}")
                    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                        endpoint=connectivity_info.host_address,
                        port=connectivity_info.port,
                        cert_filepath=args.input_cert,
                        pri_key_filepath=args.input_key,
                        ca_bytes=gg_group.certificate_authorities[0].encode('utf-8'),
                        on_connection_interrupted=on_connection_interupted,
                        on_connection_resumed=on_connection_resumed,
                        client_id=args.input_thing_name,
                        clean_session=False,
                        keep_alive_secs=30)

                    connect_future = mqtt_connection.connect()
                    connect_future.result()
                    print('Connected!')
                    return mqtt_connection

                except Exception as e:
                    print('Connection failed with exception {}'.format(e))
                    continue

    exit('All connection attempts failed')


mqtt_connection = try_iot_endpoints()

if args.input_mode == 'both' or args.input_mode == 'subscribe':
    def on_publish(topic, payload, dup, qos, retain, **kwargs):
        print('Publish received on topic {}'.format(topic))
        print(payload)
    subscribe_future, _ = mqtt_connection.subscribe(args.input_topic, QoS.AT_MOST_ONCE, on_publish)
    subscribe_result = subscribe_future.result()

loop_count = 0
while loop_count < args.input_max_pub_ops:
    if args.input_mode == 'both' or args.input_mode == 'publish':
        message = {}
        message['message'] = args.input_message
        message['sequence'] = loop_count
        messageJson = json.dumps(message)
        pub_future, _ = mqtt_connection.publish(args.input_topic, messageJson, QoS.AT_LEAST_ONCE)
        publish_completion_data = pub_future.result()
        print('Successfully published to topic {} with payload `{}`\n'.format(args.input_topic, messageJson))

        loop_count += 1
    time.sleep(1)