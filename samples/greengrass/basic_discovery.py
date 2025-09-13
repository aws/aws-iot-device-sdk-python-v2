# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot.greengrass_discovery import DiscoveryClient
from awsiot import mqtt_connection_builder
from awscrt import io, http
from awscrt.mqtt import QoS
import time, json

allowed_actions = ['both', 'publish', 'subscribe']

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

parser = argparse.ArgumentParser(
    description="Greengrass Basic Discovery",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
required = parser.add_argument_group("required arguments")
optional = parser.add_argument_group("optional arguments")

# Required Arguments
required.add_argument("--cert", required=True,  metavar="", dest="input_cert",
                    help="Path to the certificate file to use during mTLS connection establishment")
required.add_argument("--key", required=True,  metavar="", dest="input_key",
                    help="Path to the private key file to use during mTLS connection establishment")
required.add_argument("--region", required=True,  metavar="", dest="input_signing_region",
                      help="The region to connect through.")
required.add_argument("--thing_name", required=True,  metavar="", dest="input_thing_name",
                      help="The name assigned to your IoT Thing.")

# Optional Arguments
optional.add_argument("--ca_file",  metavar="", dest="input_ca",
                      help="Path to optional CA bundle (PEM)")
optional.add_argument("--topic", default=f"test/topic/{uuid.uuid4().hex[:8]}",  metavar="", dest="input_topic",
                      help="Topic")
optional.add_argument("--message", default="Hello World!",  metavar="", dest="input_message",
                      help="Message payload")
optional.add_argument("--max_pub_ops", type=int, default=10,  metavar="", dest="input_max_pub_ops", 
                    help="The maximum number of publish operations (optional, default='10').")
optional.add_argument("--print_discover_resp_only", type=bool, default=False,  metavar="", dest="input_print_discovery_resp_only",
                    help="(optional, default='False').")
optional.add_argument("--mode", default='both',  metavar="", dest="input_mode",
                    help=f"The operation mode (optional, default='both').\nModes:{allowed_actions}")
optional.add_argument("--proxy_host",  metavar="", dest="input_proxy_host",
                      help="HTTP proxy host")
optional.add_argument("--proxy_port", type=int, default=0,  metavar="", dest="input_proxy_port",
                      help="HTTP proxy port")
optional.add_argument("--client_id",  metavar="", dest="input_clientId", default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}",
                    help="Client ID")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------


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