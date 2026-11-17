# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# Tests of reconnecting an event-stream RPC connection (e.g. to a restarted
# Greengrass nucleus) with a token that may change between connections.
# The socket layer is mocked, so these tests do not need an echo server.

from concurrent.futures import Future
import json
from typing import List, Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch

from awscrt.eventstream.rpc import MessageFlag, MessageType

import awsiot.greengrasscoreipc
from awsiot.eventstreamrpc import Client, Connection, LifecycleHandler, MessageAmendment, ShapeIndex

TIMEOUT = 10.0


class RecordingLifecycleHandler(LifecycleHandler):
    def __init__(self):
        self.connects = 0
        self.disconnect_reasons = []  # type: List[Optional[Exception]]

    def on_connect(self):
        self.connects += 1

    def on_disconnect(self, reason):
        self.disconnect_reasons.append(reason)


def _auth_token_of(amendment: MessageAmendment) -> str:
    return json.loads(amendment.payload.decode())["authToken"]


class AuthTokenAmenderTest(TestCase):

    def test_static_amender_payload_is_unchanged(self):
        amender = MessageAmendment.create_static_authtoken_amender("abc")
        self.assertEqual(b'{"authToken": "abc"}', amender().payload)

    def test_static_amender_payload_is_valid_json_for_any_token(self):
        token = 'with "quotes" and \\ backslash'
        amender = MessageAmendment.create_static_authtoken_amender(token)
        self.assertEqual(token, _auth_token_of(amender()))

    def test_amender_asks_the_provider_for_the_token_on_every_call(self):
        tokens = iter(["first", "second"])
        amender = MessageAmendment.create_authtoken_amender(lambda: next(tokens))

        self.assertEqual("first", _auth_token_of(amender()))
        self.assertEqual("second", _auth_token_of(amender()))


class FakeServer:
    """
    Plays the server side of the protocol by invoking the callbacks the
    Connection registered with the (mocked) awscrt ClientConnection.connect().
    """

    def __init__(self, crt_connect: MagicMock):
        self._crt_connect = crt_connect
        self.crt_connection = MagicMock()

    @property
    def _handler(self):
        return self._crt_connect.call_args.kwargs["handler"]

    def accept(self):
        self._handler.on_connection_setup(connection=self.crt_connection, error=None)
        self._handler.on_protocol_message(
            headers=[], payload=b"", message_type=MessageType.CONNECT_ACK, flags=MessageFlag.CONNECTION_ACCEPTED)

    def close_connection(self, reason: Optional[Exception] = None):
        self._handler.on_connection_shutdown(reason=reason)

    def refuse_socket(self, error: Exception):
        self._handler.on_connection_setup(connection=None, error=error)

    def last_auth_token(self) -> str:
        payload = self.crt_connection.send_protocol_message.call_args.kwargs["payload"]
        return json.loads(payload.decode())["authToken"]

    def lifecycle_handler_of_last_connect(self) -> LifecycleHandler:
        return self._handler.lifecycle_handler


@patch("awsiot.eventstreamrpc.protocol.ClientConnection.connect")
class ConnectionReconnectTest(TestCase):

    def _connection(self, authtoken_provider=lambda: "token") -> Connection:
        return Connection(
            host_name="/path/to/ipc.socket",
            port=0,
            bootstrap=MagicMock(),
            connect_message_amender=MessageAmendment.create_authtoken_amender(authtoken_provider))

    def test_reconnect_before_connect_raises(self, crt_connect):
        with self.assertRaises(RuntimeError):
            self._connection().reconnect()

    def test_reconnect_while_connected_raises(self, crt_connect):
        server = FakeServer(crt_connect)
        connection = self._connection()
        future = connection.connect(RecordingLifecycleHandler())
        server.accept()
        future.result(TIMEOUT)

        with self.assertRaises(RuntimeError):
            connection.reconnect()

    def test_reconnect_after_the_server_closed_the_connection(self, crt_connect):
        server = FakeServer(crt_connect)
        tokens = iter(["token-before-restart", "token-after-restart"])
        connection = self._connection(lambda: next(tokens))
        lifecycle_handler = RecordingLifecycleHandler()

        first = connection.connect(lifecycle_handler)
        server.accept()
        first.result(TIMEOUT)
        self.assertEqual("token-before-restart", server.last_auth_token())

        closed_reason = RuntimeError("AWS_IO_SOCKET_CLOSED")
        server.close_connection(closed_reason)
        self.assertEqual([closed_reason], lifecycle_handler.disconnect_reasons)

        second = connection.reconnect()
        server.accept()

        self.assertIsNone(second.result(TIMEOUT))
        self.assertIs(lifecycle_handler, server.lifecycle_handler_of_last_connect())
        self.assertEqual("token-after-restart", server.last_auth_token())
        self.assertEqual(2, lifecycle_handler.connects)
        self.assertEqual(2, crt_connect.call_count)

    def test_reconnect_after_a_failed_attempt(self, crt_connect):
        # e.g. the server is still restarting: the application keeps retrying
        server = FakeServer(crt_connect)
        connection = self._connection()
        lifecycle_handler = RecordingLifecycleHandler()

        refused = RuntimeError("AWS_IO_SOCKET_CONNECTION_REFUSED")
        first = connection.connect(lifecycle_handler)
        server.refuse_socket(refused)
        self.assertIs(refused, first.exception(TIMEOUT))

        second = connection.reconnect()
        server.accept()

        self.assertIsNone(second.result(TIMEOUT))
        self.assertEqual(1, lifecycle_handler.connects)

    def test_client_reconnect_reopens_its_connection(self, crt_connect):
        server = FakeServer(crt_connect)
        connection = self._connection()
        client = Client(connection, ShapeIndex([]))
        connection.connect(RecordingLifecycleHandler())
        server.accept()
        server.close_connection()

        reconnected = client.reconnect()
        server.accept()

        self.assertIsNone(reconnected.result(TIMEOUT))


@patch("awsiot.greengrasscoreipc.Connection")
class GreengrassCoreIpcConnectTest(TestCase):

    def _connect(self, connection_class: MagicMock, authtoken) -> MessageAmendment:
        connected = Future()
        connected.set_result(None)
        connection_class.return_value.connect.return_value = connected

        awsiot.greengrasscoreipc.connect(ipc_socket="/path/to/ipc.socket", authtoken=authtoken)

        return connection_class.call_args.kwargs["connect_message_amender"]

    def test_string_authtoken_is_sent_on_every_connection(self, connection_class):
        amender = self._connect(connection_class, "static-token")

        self.assertEqual("static-token", _auth_token_of(amender()))
        self.assertEqual("static-token", _auth_token_of(amender()))

    def test_callable_authtoken_is_called_on_every_connection(self, connection_class):
        tokens = iter(["first-token", "second-token"])
        amender = self._connect(connection_class, lambda: next(tokens))

        self.assertEqual("first-token", _auth_token_of(amender()))
        self.assertEqual("second-token", _auth_token_of(amender()))
