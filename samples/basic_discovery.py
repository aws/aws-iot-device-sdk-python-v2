# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from concurrent.futures import Future
from awscrt import io
from awscrt.io import Logger, LogLevel
from awsiot.greengrass_discovery import DiscoveryClient, DiscoverResponse

logger = Logger(LogLevel.Trace, '/home/ANT.AMAZON.COM/henso/source/log.out')
event_loop_group = io.EventLoopGroup(1)
client_bootstrap = io.ClientBootstrap(event_loop_group)

tls_options = io.TlsContextOptions.create_client_with_mtls_from_path('/home/ANT.AMAZON.COM/henso/source/93db7f84e6.cert.pem', '/home/ANT.AMAZON.COM/henso/source/93db7f84e6.private.key')
tls_options.override_default_trust_store_from_path(None, '/home/ANT.AMAZON.COM/henso/source/AmazonRootCA1.pem')
tls_context = io.ClientTlsContext(tls_options)

socket_options = io.SocketOptions()
socket_options.connect_timeout_ms = 3000

discovery_client = DiscoveryClient(client_bootstrap, socket_options, tls_context, 'us-east-1')
resp_future = discovery_client.discover('HelloWorld_Publisher')
resp = resp_future.result()

print(resp)
