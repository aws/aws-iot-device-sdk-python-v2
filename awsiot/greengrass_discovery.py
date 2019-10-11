# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from awscrt.http import HttpClientConnection, HttpRequest
from awscrt.io import ClientBootstrap, ClientTlsContext, is_alpn_available, SocketOptions, TlsConnectionOptions
import awsiot
from concurrent.futures import Future
import json

class DiscoveryClient(object):
    __slots__ = ['_bootstrap', '_tls_context', '_socket_options', '_region', '_tls_connection_options', '_gg_server_name', 'gg_url', 'port']

    def __init__(self, bootstrap, socket_options, tls_context, region):
        assert bootstrap is not None and isinstance(bootstrap, ClientBootstrap)
        assert socket_options is not None and isinstance(socket_options, SocketOptions)
        assert tls_context is not None and isinstance(tls_context, ClientTlsContext)
        assert region is not None and isinstance(region, str)

        self._bootstrap = bootstrap
        self._socket_options = socket_options
        self._region = region
        self._gg_server_name = 'greengrass-ats.iot.{}.amazonaws.com'.format(region)
        self._tls_connection_options = tls_context.new_connection_options()
        self._tls_connection_options.set_server_name(self._gg_server_name)
        self.port = 8443

        if is_alpn_available():
            self._tls_connection_options.set_alpn_list(['x-amzn-http-ca'])
            self.port = 443

    def discover(self, thing_name):

        discovery = dict(
            future=Future(),
            response_body=bytearray())

        def on_incoming_body(http_stream, response_chunk):
            discovery['response_body'].extend(response_chunk)

        def on_request_complete(completion_future):
            try:
                response_code = completion_future.result()
                if response_code == 200:
                    payload_str = discovery['response_body'].decode('utf-8')
                    discover_res = DiscoverResponse.from_payload(json.loads(payload_str))
                    discovery['future'].set_result(discover_res)
                else:
                    discovery['future'].set_exception(DiscoveryException('Error during discover call: response_code={}'.format(response_code), response_code))

            except Exception as e:
                discovery['future'].set_exception(e)

        def on_connection_completed(conn_future):
            try:
                connection = conn_future.result()
                request = HttpRequest(
                    method='GET',
                    path='/greengrass/discover/thing/{}'.format(thing_name),
                    headers=[('host', self._gg_server_name)])

                http_stream = connection.request(
                    request=request,
                    on_body=on_incoming_body)

                http_stream.completion_future.add_done_callback(on_request_complete)

            except Exception as e:
                discovery['future'].set_exception(e)

        connect_future = HttpClientConnection.new(
            host_name=self._gg_server_name,
            port=self.port,
            socket_options=self._socket_options,
            tls_connection_options = self._tls_connection_options,
            bootstrap = self._bootstrap)

        connect_future.add_done_callback(on_connection_completed)

        return discovery['future']

class DiscoveryException(Exception):
    _slots_ = ['http_response_code', 'message']

    def __init__(self, message, response_code):
        self.http_response_code = response_code
        self.message = message


class ConnectivityInfo(awsiot.ModeledClass):
    __slots__ = ['id', 'host_address', 'metadata', 'port']

    def ___init___(self):
        for slot in self.__slots__:
            setattr(self, slot, None)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ConnectivityInfo
        new = cls()
        val = payload.get('Id')
        if val is not None:
            new.id = val
        val = payload.get('HostAddress')
        if val is not None:
            new.host_address = val
        val = payload.get('PortNumber')
        if val is not None:
            new.port = val
        val = payload.get('Metadata')
        if val is not None:
            new.metadata = val
        return new

class GGCore(awsiot.ModeledClass):
    __slots__ = ['thing_arn', 'connectivity']

    def ___init___(self):
        for slot in self.__slots__:
            setattr(self, slot, None)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> GGCore
        new = cls()
        val = payload.get('thingArn')
        if val is not None:
            new.thing_arn = val
        val = payload.get('Connectivity')
        if val is not None:
            new.connectivity = [ConnectivityInfo.from_payload(i) for i in val]

        return new

class GGGroup(awsiot.ModeledClass):
    __slots__ = ['gg_group_id', 'cores', 'certificate_authorities']

    def ___init___(self):
       for slot in self.__slots__:
           setattr(self, slot, None)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> GGGroup
        new = cls()
        val = payload.get('GGGroupId')
        if val is not None:
            new.gg_group_id = val
        val = payload.get('Cores')
        if val is not None:
            new.cores = [GGCore.from_payload(i) for i in val]
        val = payload.get('CAs')
        if val is not None:
            new.certificate_authorities = val

        return new

class DiscoverResponse(awsiot.ModeledClass):
    __slots__ = ['gg_groups']

    def ___init___(self):
        for slot in self.__slots__:
            setattr(self, slot, None)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> DiscoverResponse
        new = cls()
        val = payload.get('GGGroups')
        if val is not None:
            new.gg_groups = [GGGroup.from_payload(i) for i in val]

        return new
