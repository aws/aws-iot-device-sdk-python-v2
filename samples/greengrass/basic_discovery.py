# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot.greengrass_discovery import DiscoveryClient
from awsiot import mqtt5_client_builder
from awscrt import mqtt5, io
import time, json, threading

allowed_actions = ['both', 'publish', 'subscribe']

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

parser = argparse.ArgumentParser(
    description="Greengrass Basic Discovery",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
# Connection / TLS
parser.add_argument("--cert", required=True, dest="input_cert",
                    help="Path to the certificate file to use during mTLS connection establishment")
parser.add_argument("--key", required=True, dest="input_key",
                    help="Path to the private key file to use during mTLS connection establishment")
parser.add_argument("--ca_file", dest="input_ca", help="Path to optional CA bundle (PEM)")
parser.add_argument("--region", required=True, dest="input_signing_region", help="The region to connect through.")
parser.add_argument("--thing_name", required=True, dest="input_thing_name", help="The name assigned to your IoT Thing.")

# Optional Arguments
parser.add_argument("--max_pub_ops", type=int, default=10, dest="input_max_pub_ops", 
                    help="The maximum number of publish operations (optional, default='10').")
parser.add_argument("--print_discover_resp_only", type=bool, default=False, dest="input_print_discovery_resp_only", 
                    help="(optional, default='False').")
parser.add_argument("--mode", default='both', dest="input_mode", 
                    help=f"The operation mode (optional, default='both').\nModes:{allowed_actions}")

# Proxy
parser.add_argument("--proxy-host", dest="input_proxy_host", help="HTTP proxy host")
parser.add_argument("--proxy-port", type=int, default=0, dest="input_proxy_port", help="HTTP proxy port")

parser.add_argument("--client-id", dest="input_clientId", default=f"mqtt5-sample-{uuid.uuid4().hex[:8]}", help="Client ID")
parser.add_argument("--topic", default=f"test/topic/{uuid.uuid4().hex[:8]}", dest="input_topic", help="Topic")
parser.add_argument("--message", default="Hello World!", dest="input_message", help="Message payload")
parser.add_argument("--count", default=5, dest="input_count", help="Messages to publish (0 = infinite)")

# args contains all the parsed commandline arguments used by the sample
args = parser.parse_args()
# --------------------------------- ARGUMENT PARSING END -----------------------------------------

connection_success_event = threading.Event()
TIMEOUT = 20

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(args.input_cert, args.input_key)
if (args.input_ca is not None):
    tls_options.override_default_trust_store_from_path(None, args.input_ca)
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()

proxy_options = None
if args.input_proxy_host is not None and args.input_proxy_port != 0:
    proxy_options = http.HttpProxyOptions(args.input_proxy_host, args.input_proxy_port)

print(f'Performing greengrass discovery for thing: {args.input_thing_name}...')
discovery_client = DiscoveryClient(
    io.ClientBootstrap.get_or_create_static_default(),
    socket_options,
    tls_context,
    args.input_signing_region, 
    None, 
    proxy_options)
resp_future = discovery_client.discover(args.input_thing_name)
discover_response = resp_future.result()

print("Received a greengrass discovery result! Not showing result for possible data sensitivity.")

if (args.input_print_discovery_resp_only):
    exit(0)


def on_lifecycle_disconnection(lifecycle_disconnection_data: mqtt5.LifecycleDisconnectionData):
    print("connection interrupted with error {}"
          .format(repr(lifecycle_disconnection_data.disconnect_packet.reason_code)))

# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    connack_packet = lifecycle_connect_success_data.connack_packet
    
    if connack_packet.session_present:
        print('session resumed with reason code {}'
              .format(repr(connack_packet.reason_code)))
    else:
        print("Lifecycle Connection Success with reason_code:{}\n".format(
            repr(connack_packet.reason_code)))
        connection_success_event.set()

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    print("Received new message on topic {}".format(publish_packet.topic))
    print("{}".format(publish_packet.payload.decode('utf-8')))

# Try IoT endpoints until we find one that works
def try_iot_endpoints():
    for gg_group in discover_response.gg_groups:
        for gg_core in gg_group.cores:
            for connectivity_info in gg_core.connectivity:
                try:
                    print(
                        f"Trying core {gg_core.thing_arn} at host {connectivity_info.host_address} port {connectivity_info.port}")
                    mqtt5_client = mqtt5_client_builder.mtls_from_path(
                        endpoint=connectivity_info.host_address,
                        port=connectivity_info.port,
                        cert_filepath=args.input_cert,
                        pri_key_filepath=args.input_key,
                        ca_bytes=gg_group.certificate_authorities[0].encode('utf-8'),
                        on_lifecycle_disconnection=on_lifecycle_disconnection,
                        on_lifecycle_connection_success=on_lifecycle_connection_success,
                        on_publish_received=on_publish_received,
                        client_id=args.input_thing_name,
                        clean_session=False,
                        keep_alive_interval_sec=30)
                    
                    mqtt5_client.start()
                    if not connection_success_event.wait(TIMEOUT):
                        raise TimeoutError("Connection timeout")
                    
                    return mqtt5_client

                except Exception as e:
                    print('Connection failed with exception {}'.format(e))
                    continue

    exit('All connection attempts failed')


mqtt5_client = try_iot_endpoints()

if args.input_mode == 'both' or args.input_mode == 'subscribe':

    subscribe_future = mqtt5_client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
        subscriptions=[mqtt5.Subscription(
            topic_filter=args.input_topic,
            qos=mqtt5.QoS.AT_MOST_ONCE)]
    ))
    suback = subscribe_future.result(TIMEOUT)
    print("Successfully subscribed to topic {}".format(args.input_topic))

print(f"Starting publishing loop with mode: {args.input_mode}, max_ops: {args.input_max_pub_ops}")
loop_count = 0
while loop_count < args.input_max_pub_ops:
    if args.input_mode == 'both' or args.input_mode == 'publish':
        message = {}
        message['message'] = args.input_message
        message['sequence'] = loop_count
        messageJson = json.dumps(message)

        print(f"Publishing message {loop_count + 1}/{args.input_max_pub_ops} to topic {args.input_topic}")
        publish_future = mqtt5_client.publish(mqtt5.PublishPacket(
            topic=args.input_topic,
            payload=messageJson,
            qos=mqtt5.QoS.AT_LEAST_ONCE
        ))
        publish_completion_data = publish_future.result(TIMEOUT)
        print("Successfully published to topic {} with payload `{}`\n".format(args.input_topic, messageJson))

        loop_count += 1
    else:
        print(f"Skipping publish due to mode: {args.input_mode}")
        break
    time.sleep(1)

print(f"Publishing loop completed. Published {loop_count} messages.")