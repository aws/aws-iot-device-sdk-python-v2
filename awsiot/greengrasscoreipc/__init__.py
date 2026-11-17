# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import os
from typing import Callable, Optional, Union

from awscrt.io import (
    ClientBootstrap,
    DefaultHostResolver,
    EventLoopGroup,
    SocketDomain,
    SocketOptions,
)
from awsiot.eventstreamrpc import (
    Connection,
    LifecycleHandler,
    MessageAmendment,
)
from awsiot.greengrasscoreipc.client import GreengrassCoreIPCClient


def connect(*,
            ipc_socket: str=None,
            authtoken: Optional[Union[str, Callable[[], str]]]=None,
            lifecycle_handler: Optional[LifecycleHandler]=None,
            timeout: float=10.0) -> GreengrassCoreIPCClient:
    """
    Creates an IPC client and connects to the GreengrassCoreIPC service.  When finished with the client,
    you must call close() to free the client's native resources.

    The client does not reconnect by itself: once the connection is closed (e.g. because the
    Greengrass nucleus restarted), every new operation fails with
    :class:`awsiot.eventstreamrpc.ConnectionClosedError`. Call
    :meth:`~awsiot.eventstreamrpc.Client.reconnect` (``client.reconnect()``, or
    ``client_v2.client.reconnect()`` for a :class:`~awsiot.greengrasscoreipc.clientv2.GreengrassCoreIPCClientV2`)
    to open the connection again, e.g. when
    :meth:`~awsiot.eventstreamrpc.LifecycleHandler.on_disconnect` is invoked (do not block on the
    returned future inside that callback). Streaming operations such as subscriptions must then be
    created again.

    Args:
        ipc_socket: Path to the Unix domain socket of Greengrass Nucleus, defaults to
            environment variable AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT
        authtoken: Authentication token, defaults to environment variable SVCUID.
            Either a string, used for every connection, or a callable returning the token,
            called every time a connection is established, including reconnects. Use a
            callable when the token can change while the application runs, e.g. for a
            process that is not started by the nucleus and must reconnect with the token
            the nucleus issues after it restarts.
        lifecycle_handler: Handler for events over the course of this
            network connection. See :class:`awsiot.eventstreamrpc.LifecycleHandler` for more info.
            Handler methods will only be invoked if the connect attempt
            succeeds.
        timeout: The number of seconds to wait for establishing the connection.

    Returns:
        Client for the GreengrassCoreIPC service.
    """

    if not ipc_socket:
        ipc_socket = os.environ["AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT"]
    if not authtoken:
        authtoken = os.environ["SVCUID"]
    if not lifecycle_handler:
        lifecycle_handler = LifecycleHandler()

    elg = EventLoopGroup(num_threads=1)
    resolver = DefaultHostResolver(elg)
    bootstrap = ClientBootstrap(elg, resolver)
    socket_options = SocketOptions()
    socket_options.domain = SocketDomain.Local
    if callable(authtoken):
        amender = MessageAmendment.create_authtoken_amender(authtoken)
    else:
        amender = MessageAmendment.create_static_authtoken_amender(authtoken)

    connection = Connection(
        host_name=ipc_socket,
        port=0, # dummy port number, not needed for Unix domain sockets
        bootstrap=bootstrap,
        socket_options=socket_options,
        connect_message_amender=amender,
    )
    connect_future = connection.connect(lifecycle_handler)
    connect_future.result(timeout)

    return GreengrassCoreIPCClient(connection)
