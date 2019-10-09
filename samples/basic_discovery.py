# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License').
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the 'license' file accompanying this file. This file is distributed
# on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import argparse
import time
import uuid
import json
from concurrent.futures import Future
from awscrt import io
from awscrt.io import LogLevel
from awscrt.mqtt import Connection, Client, QoS
from awsiot.greengrass_discovery import DiscoveryClient, DiscoverResponse

allowed_actions = ['both', 'publish', 'subscribe']

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--ca_file', action='store', required=True, dest='root_ca_path', help='Root CA file path')
parser.add_argument('-c', '--cert', action='store', required=True, dest='certificate_path', help='Certificate file path')
parser.add_argument('-k', '--key', action='store', required=True, dest='private_key_path', help='Private key file path')
parser.add_argument('-n', '--thing_name', action='store', required=True, dest='thing_name', help='Targeted thing name')
parser.add_argument('-t', '--topic', action='store', dest='topic', default='sdk/test/Python', help='Targeted topic')
parser.add_argument('-m', '--mode', action='store', dest='mode', default='both',
                    help='Operation modes: %s'%str(allowed_actions))
parser.add_argument('-M', '--message', action='store', dest='message', default='Hello World!',
help='Message to publish')
parser.add_argument('--region', action='store', dest='region', default='us-east-1')
parser.add_argument('--max_pub_ops', action='store', dest='max_pub_ops', default=10)
parser.add_argument('--print_discover_resp_only', action='store_true', dest='print_discover_resp_only', default=False)
parser.add_argument('-v', '--verbose', action='store', dest='verbosity', default='NoLogs')

args = parser.parse_args()

if args.verbosity.lower() == 'fatal':
    io.init_logging(LogLevel.Fatal, 'stderr')
elif args.verbosity.lower() == 'error':
    io.init_logging(LogLevel.Error, 'stderr')
elif args.verbosity.lower() == 'warn':
    io.init_logging(LogLevel.Warn, 'stderr')
elif args.verbosity.lower() == 'info':
    io.init_logging(LogLevel.Info, 'stderr')
elif args.verbosity.lower() == 'debug':
    io.init_logging(LogLevel.Debug, 'stderr')
elif args.verbosity.lower() == 'trace':
    io.init_logging(LogLevel.Trace, 'stderr')

event_loop_group = io.EventLoopGroup(1)
client_bootstrap = io.ClientBootstrap(event_loop_group)

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.certificate_path, args.private_key_path)
tls_options.override_default_trust_store_from_path(None, args.root_ca_path)
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()
socket_options.connect_timeout_ms = 3000

discovery_client = DiscoveryClient(client_bootstrap, socket_options, tls_context, args.region)
resp_future = discovery_client.discover(args.thing_name)
resp = resp_future.result()

if args.print_discover_resp_only:
    print(resp)
    exit(0)

gg_core_tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.certificate_path, args.private_key_path)
gg_core_tls_options.override_default_trust_store(bytes(resp.gg_groups[0].certificate_authorities[0], encoding='utf-8'))
gg_core_tls_ctx = io.ClientTlsContext(gg_core_tls_options)
mqtt_client = Client(client_bootstrap, gg_core_tls_ctx)


def on_connection_interupted(connection, error_code):
    print('connection interupted with error {}'.format(error_code))


def on_connection_resumed(connection, error_code, session_present):
    print('connection resumed with error {}, session present {}'.format(error_code, session_present))


mqtt_connection = Connection(mqtt_client, on_connection_interrupted=on_connection_interupted, on_connection_resumed=on_connection_resumed)

connection_succeeded = False
for conectivity_info in resp.gg_groups[0].cores[0].connectivity:
    try:
        connect_future = mqtt_connection.connect(args.thing_name, resp.gg_groups[0].cores[0].connectivity[0].host_address, resp.gg_groups[0].cores[0].connectivity[0].port, clean_session=False)
        connect_future.result()
        connection_succeeded = True
        break
    except Exception as e:
        print('connection failed with exception {}'.format(e))
        continue

if connection_succeeded != True:
    print('All connection attempts for core {} failed'.format(resp.gg_groups[0].cores[0].thing_arn))
    exit(-1)

if args.mode == 'both' or args.mode == 'subscribe':

    def on_publish(topic, message):
        print('publish recieved on topic {}'.format(topic))
        print(message)

    subscribe_future = mqtt_connection.subscribe(args.topic, QoS.AT_MOST_ONCE, on_publish)
    subscribe_future[0].result()

loop_count = 0
while loop_count < args.max_pub_ops:
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = args.message
        message['sequence'] = loop_count
        messageJson = json.dumps(message)
        pub_future = mqtt_connection.publish(args.topic, messageJson, QoS.AT_MOST_ONCE)
        pub_future[0].result()
        print('Published topic {}: {}\n'.format(args.topic, messageJson))

        loop_count += 1
    time.sleep(1)
