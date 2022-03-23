# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt.http import HttpClientConnection, HttpRequest, HttpHeaders
from awscrt.io import ClientBootstrap, ClientTlsContext, is_alpn_available, SocketOptions, TlsConnectionOptions
import awsiot
from concurrent.futures import Future
import json
from typing import Any, Dict, List, Optional


class DiscoveryClient:
    """
    Client which performs Greengrass discovery.

    Args:
        bootstrap: Client bootstrap
        socket_options: Socket options
        tls_context: Client TLS context
        region: AWS region (not used if gg_server_name is set)
        gg_server_name: optional full server name
    """
    __slots__ = [
        '_bootstrap',
        '_tls_context',
        '_socket_options',
        '_region',
        '_tls_connection_options',
        '_gg_server_name',
        'gg_url',
        'port']

    def __init__(
            self,
            bootstrap: ClientBootstrap,
            socket_options: SocketOptions,
            tls_context: ClientTlsContext,
            region: str,
            gg_server_name: str = None):
        assert isinstance(bootstrap, ClientBootstrap)
        assert isinstance(socket_options, SocketOptions)
        assert isinstance(tls_context, ClientTlsContext)
        assert isinstance(region, str)
        if gg_server_name is not None: 
            assert isinstance(gg_server_name, str)

        self._bootstrap = bootstrap
        self._socket_options = socket_options
        self._region = region
        if gg_server_name is None:
            self._gg_server_name = 'greengrass-ats.iot.{}.amazonaws.com'.format(region)
        else:
            self._gg_server_name = gg_server_name

        self._tls_connection_options = tls_context.new_connection_options()
        self._tls_connection_options.set_server_name(self._gg_server_name)
        self.port = 8443

        if is_alpn_available():
            self._tls_connection_options.set_alpn_list(['x-amzn-http-ca'])
            self.port = 443

    def discover(self, thing_name: str) -> Future:
        """
        Perform discovery.

        This is an asynchronous operation.

        Returns:
            Future a Future which will contain a result of :class:`DiscoverResponse`
            on success, or an exception on failure.
        """

        discovery = dict(
            future=Future(),
            response_body=bytearray())

        def on_incoming_body(http_stream, chunk, **kwargs):
            discovery['response_body'].extend(chunk)

        def on_request_complete(completion_future):
            try:
                response_code = completion_future.result()
                if response_code == 200:
                    payload_str = discovery['response_body'].decode('utf-8')
                    discover_res = DiscoverResponse.from_payload(json.loads(payload_str))
                    discovery['future'].set_result(discover_res)
                else:
                    discovery['future'].set_exception(
                        DiscoveryException(
                            'Error during discover call: response_code={}'.format(response_code),
                            response_code))

            except Exception as e:
                discovery['future'].set_exception(e)

        def on_connection_completed(conn_future):
            try:
                connection = conn_future.result()
                headers = HttpHeaders()
                headers.add('host', self._gg_server_name)
                request = HttpRequest(
                    method='GET',
                    path='/greengrass/discover/thing/{}'.format(thing_name),
                    headers=headers)

                http_stream = connection.request(
                    request=request,
                    on_body=on_incoming_body)

                http_stream.activate()
                http_stream.completion_future.add_done_callback(on_request_complete)

            except Exception as e:
                discovery['future'].set_exception(e)

        connect_future = HttpClientConnection.new(
            host_name=self._gg_server_name,
            port=self.port,
            socket_options=self._socket_options,
            tls_connection_options=self._tls_connection_options,
            bootstrap=self._bootstrap)

        connect_future.add_done_callback(on_connection_completed)

        return discovery['future']


class DiscoveryException(Exception):
    """
    Discovery response was an error.
    """
    _slots_ = ['http_response_code', 'message']

    def __init__(self, message: str, response_code:int):
        #: HTTP response code
        self.http_response_code = response_code # type: int
        #: Message
        self.message = message # type: str


class ConnectivityInfo(awsiot.ModeledClass):
    """
    Connectivity info
    """

    __slots__ = ['id', 'host_address', 'metadata', 'port']
    def __init__(self):
        #: ID
        self.id = None
        #: Port address
        self.host_address = None
        #: Metadata
        self.metadata = None
        #: Port
        self.port = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> 'ConnectivityInfo':
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
    """
    Greengrass Core
    """
    __slots__ = ['thing_arn', 'connectivity']

    def __init__(self):
        #: Thing ARN
        self.thing_arn = None
        #: List of :class:`ConnectivityInfo`
        self.connectivity = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> 'GGCore':
        new = cls()
        val = payload.get('thingArn')
        if val is not None:
            new.thing_arn = val
        val = payload.get('Connectivity')
        if val is not None:
            new.connectivity = [ConnectivityInfo.from_payload(i) for i in val]

        return new


class GGGroup(awsiot.ModeledClass):
    """
    Greengrass group
    """
    __slots__ = ['gg_group_id', 'cores', 'certificate_authorities']

    def __init__(self):
        #: Greengrass group ID
        self.gg_group_id = None
        #: List of :class:`GGCore`
        self.cores = None
        #: List of strings
        self.certificate_authorities = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> 'GGGroup':
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
    """
    Discovery response
    """
    __slots__ = ['gg_groups']

    def __init__(self):
        #: List of :class:`GGGroup`
        self.gg_groups = None # type: Optional[List[GGGroup]]

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> 'DiscoverResponse':
        new = cls()
        val = payload.get('GGGroups')
        if val is not None:
            new.gg_groups = [GGGroup.from_payload(i) for i in val]

        return new
