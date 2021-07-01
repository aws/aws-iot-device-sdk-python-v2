# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
import time
import uuid
import json
from concurrent.futures import Future
from awscrt import io
from awscrt.io import LogLevel
from awscrt.mqtt import Connection, Client, QoS
from awsiot.greengrass_discovery import DiscoveryClient, DiscoverResponse
from awsiot import mqtt_connection_builder

allowed_actions = ['both', 'publish', 'subscribe']

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--root-ca', action='store', dest='root_ca_path', help='Root CA file path')
parser.add_argument('-c', '--cert', action='store', required=True, dest='certificate_path', help='Certificate file path')
parser.add_argument('-k', '--key', action='store', required=True, dest='private_key_path', help='Private key file path')
parser.add_argument('-n', '--thing-name', action='store', required=True, dest='thing_name', help='Targeted thing name')
parser.add_argument('-t', '--topic', action='store', dest='topic', default='test/topic', help='Targeted topic')
parser.add_argument('-m', '--mode', action='store', dest='mode', default='both',
                    help='Operation modes: %s'%str(allowed_actions))
parser.add_argument('-M', '--message', action='store', dest='message', default='Hello World!',
                    help='Message to publish')
parser.add_argument('--region', action='store', dest='region', default='us-east-1')
parser.add_argument('--max-pub-ops', action='store', dest='max_pub_ops', default=10)
parser.add_argument('--print-discover-resp-only', action='store_true', dest='print_discover_resp_only', default=False)
parser.add_argument('-v', '--verbosity', choices=[x.name for x in LogLevel], default=LogLevel.NoLogs.name,
                    help='Logging level')

args = parser.parse_args()

io.init_logging(getattr(LogLevel, args.verbosity), 'stderr')

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.certificate_path, args.private_key_path)
if args.root_ca_path:
    tls_options.override_default_trust_store_from_path(None, args.root_ca_path)
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()

print('Performing greengrass discovery...')
discovery_client = DiscoveryClient(client_bootstrap, socket_options, tls_context, args.region)
resp_future = discovery_client.discover(args.thing_name)
discover_response = resp_future.result()

print(discover_response)
if args.print_discover_resp_only:
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
                    print('Trying core {} at host {} port {}'.format(gg_core.thing_arn, connectivity_info.host_address, connectivity_info.port))
                    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                        endpoint=connectivity_info.host_address,
                        port=connectivity_info.port,
                        cert_filepath=args.certificate_path,
                        pri_key_filepath=args.private_key_path,
                        client_bootstrap=client_bootstrap,
                        ca_bytes=gg_group.certificate_authorities[0].encode('utf-8'),
                        on_connection_interrupted=on_connection_interupted,
                        on_connection_resumed=on_connection_resumed,
                        client_id=args.thing_name,
                        clean_session=False,
                        keep_alive_secs=6)

                    connect_future = mqtt_connection.connect()
                    connect_future.result()
                    print('Connected!')
                    return mqtt_connection

                except Exception as e:
                    print('Connection failed with exception {}'.format(e))
                    continue

    exit('All connection attempts failed')

mqtt_connection = try_iot_endpoints()

if args.mode == 'both' or args.mode == 'subscribe':

    def on_publish(topic, payload, dup, qos, retain, **kwargs):
        print('Publish received on topic {}'.format(topic))
        print(payload)

    subscribe_future, _ = mqtt_connection.subscribe(args.topic, QoS.AT_MOST_ONCE, on_publish)
    subscribe_result = subscribe_future.result()

loop_count = 0
while loop_count < args.max_pub_ops:
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = args.message
        message['sequence'] = loop_count
        messageJson = json.dumps(message)
        pub_future, _ = mqtt_connection.publish(args.topic, messageJson, QoS.AT_MOST_ONCE)
        pub_future.result()
        print('Published topic {}: {}\n'.format(args.topic, messageJson))

        loop_count += 1
    time.sleep(1)
