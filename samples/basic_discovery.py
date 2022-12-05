# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import command_line_utils
import time
import json
from concurrent.futures import Future
from awscrt import io, http
from awscrt.mqtt import QoS
from awsiot.greengrass_discovery import DiscoveryClient
from awsiot import mqtt_connection_builder

allowed_actions = ['both', 'publish', 'subscribe']

# Parse arguments
cmdUtils = command_line_utils.CommandLineUtils("Basic Discovery - Greengrass discovery example.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.remove_command("endpoint")
cmdUtils.register_command("thing_name", "<str>", "The name assigned to your IoT Thing", required=True)
cmdUtils.register_command(
    "mode", "<mode>",
    f"The operation mode (optional, default='both').\nModes:{allowed_actions}", default='both')
cmdUtils.register_command("region", "<str>", "The region to connect through.", required=True)
cmdUtils.register_command(
    "max_pub_ops", "<int>",
    "The maximum number of publish operations (optional, default='10').",
    default=10, type=int)
cmdUtils.register_command(
    "print_discover_resp_only", "", "(optional, default='False').",
    default=False, type=bool, action="store_true")
cmdUtils.add_common_proxy_commands()
# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(
    cmdUtils.get_command_required("cert"), cmdUtils.get_command_required("key"))
if cmdUtils.get_command(cmdUtils.m_cmd_ca_file):
    tls_options.override_default_trust_store_from_path(None, cmdUtils.get_command(cmdUtils.m_cmd_ca_file))
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()

proxy_options = None
if cmdUtils.get_command(cmdUtils.m_cmd_proxy_host) != None and cmdUtils.get_command(cmdUtils.m_cmd_proxy_port) != None:
    proxy_options = http.HttpProxyOptions(
        cmdUtils.get_command_required(cmdUtils.m_cmd_proxy_host),
        cmdUtils.get_command_required(cmdUtils.m_cmd_proxy_port))

print('Performing greengrass discovery...')
discovery_client = DiscoveryClient(
    io.ClientBootstrap.get_or_create_static_default(),
    socket_options,
    tls_context,
    cmdUtils.get_command_required("region"), None, proxy_options)
resp_future = discovery_client.discover(cmdUtils.get_command_required("thing_name"))
discover_response = resp_future.result()

print(discover_response)
if cmdUtils.get_command("print_discover_resp_only"):
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
                    print (f"Trying core {gg_core.thing_arn} at host {connectivity_info.host_address} port {connectivity_info.port}")
                    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                        endpoint=connectivity_info.host_address,
                        port=connectivity_info.port,
                        cert_filepath=cmdUtils.get_command_required("cert"),
                        pri_key_filepath=cmdUtils.get_command_required("key"),
                        ca_bytes=gg_group.certificate_authorities[0].encode('utf-8'),
                        on_connection_interrupted=on_connection_interupted,
                        on_connection_resumed=on_connection_resumed,
                        client_id=cmdUtils.get_command_required("thing_name"),
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

if cmdUtils.get_command("mode") == 'both' or cmdUtils.get_command("mode") == 'subscribe':

    def on_publish(topic, payload, dup, qos, retain, **kwargs):
        print('Publish received on topic {}'.format(topic))
        print(payload)

    subscribe_future, _ = mqtt_connection.subscribe(cmdUtils.get_command("topic"), QoS.AT_MOST_ONCE, on_publish)
    subscribe_result = subscribe_future.result()

loop_count = 0
while loop_count < cmdUtils.get_command("max_pub_ops"):
    if cmdUtils.get_command("mode") == 'both' or cmdUtils.get_command("mode") == 'publish':
        message = {}
        message['message'] = cmdUtils.get_command("message")
        message['sequence'] = loop_count
        messageJson = json.dumps(message)
        pub_future, _ = mqtt_connection.publish(cmdUtils.get_command("topic"), messageJson, QoS.AT_MOST_ONCE)
        pub_future.result()
        print('Published topic {}: {}\n'.format(cmdUtils.get_command("topic"), messageJson))

        loop_count += 1
    time.sleep(1)
