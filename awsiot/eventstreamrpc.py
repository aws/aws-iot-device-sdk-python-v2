"""
Classes for building a service that uses the event-stream RPC protocol.
"""
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt.eventstream import Header, HeaderType
import awscrt.eventstream.rpc as protocol
from awscrt.io import (ClientBootstrap, SocketOptions, TlsConnectionOptions)
from concurrent.futures import Future
from enum import Enum
import json
import logging
from threading import Lock
from typing import (Any, Callable, Dict, Optional, Sequence)

VERSION_TUPLE = (0, 1, 0)
VERSION_STRING = "{v[0]}.{v[1]}.{v[2]}".format(v=VERSION_TUPLE)

VERSION_HEADER = ":version"
CONTENT_TYPE_HEADER = ":content-type"
CONTENT_TYPE_APPLICATION_TEXT = "text/plain"
CONTENT_TYPE_APPLICATION_JSON = "application/json"
SERVICE_MODEL_TYPE_HEADER = "service-model-type"


logger = logging.getLogger(__name__)


class ConnectionClosedError(RuntimeError):
    """
    Connection is closed
    """
    pass


class StreamClosedError(RuntimeError):
    """
    Stream is closed
    """
    pass


class EventStreamError(RuntimeError):
    """
    For connection-level errors.
    """
    pass


class EventStreamOperationError(RuntimeError):
    """
    Base for all errors that come across the wire.

    These are not necessarily modeled shapes.
    """
    pass


class AccessDeniedError(EventStreamOperationError):
    """
    Access Denied
    """

    def __init__(self, *args):
        super().__init__('aws#AccessDenied', *args)


class UnmappedDataError(RuntimeError):
    """
    Received data that does not map to a known model type.
    """
    pass


class SerializeError(RuntimeError):
    """
    Error serializing data to send.
    """
    pass


class DeserializeError(RuntimeError):
    """
    Error deserializing received data.
    """
    pass


class LifecycleHandler:
    """
    Base class for handling connection events.

    Inherit from this class and override methods to handle connection events.
    All callbacks for this connection will be invoked on the same thread.
    If the connection attempt fails, no callbacks will be invoked.
    If the connection attempt succeeds, :meth:`on_connect()` will be the first callback
    invoked and :meth:`on_disconnect()` will always be the last.

    Note that an open network connection MUST be closed via :meth:`Connection.close()`
    to avoid leaking resources.
    """

    def on_connect(self):
        """
        Invoked when the connection has been fully established.

        This will always be the first callback invoked on the handler.
        This will not be invoked if the connection attempt failed.
        """
        pass

    def on_disconnect(self, reason: Optional[Exception]):
        """
        Invoked when an open connection has disconnected.

        This will always be the last callback invoked on the handler.
        This will not be invoked if the connection attempt failed.

        Args:
            reason: Reason will be `None` if the user initiated the shutdown,
                otherwise the reason will be an Exception.
        """
        pass

    def on_error(self, error: Exception) -> bool:
        """
        Invoked when a connection-level error occurs.

        Args:
            reason: An Exception explaining the error

        Returns:
            True if the connection should be terminated as a result of the error,
            or False if the connection should continute.
        """
        pass

    def on_ping(self, headers: Sequence[Header], payload: bytes):
        """
        Invoked when a ping is received.
        """
        pass


class MessageAmendment:
    """
    Data to add to an event-stream message.

    Args:
        headers: Headers to add (optional)

        payload: Binary payload data (optional)
    """

    def __init__(self, *, headers: Optional[Sequence[Header]] = None, payload: Optional[bytes] = None):
        #: Headers to add
        self.headers = headers # type: Optional[Sequence[Header]]

        #: Binary payload data
        self.payload = payload # type: Optional[bytes]

    @staticmethod
    def create_static_authtoken_amender(authtoken: str) -> Callable[[], 'MessageAmendment']:
        """
        Create function that amends payload: `b'{"authToken": "..."}'`

        Args:
            authtoken: value of "authToken" in the payload.
                The same value is always used, even if the amender
                is called multiple times over the life of the application.

        Returns:
            The result is appropriate for passing to the :class:`Connection`'s
            `connect_message_amender` init arg.
        """
        def _amend():
            payload_str = '{"authToken": "%s"}' % authtoken
            return MessageAmendment(payload=payload_str.encode())

        return _amend


class _ClientState(Enum):
    DISCONNECTED = 1
    CONNECTING_TO_SOCKET = 2
    WAITING_FOR_CONNECT_ACK = 3
    CONNECTED = 4
    DISCONNECTING = 5


class _ProtocolConnectionHandler(protocol.ClientConnectionHandler):
    def __init__(self, owner, lifecycle_handler):
        self.owner = owner
        self.lifecycle_handler = lifecycle_handler

    def on_connection_setup(self, connection, error, **kwargs):
        # if error is set, socket connection failed
        if error:
            logger.error("%r failed to establish connection: %r", self.owner, error)
            synced = self.owner._synced
            with synced.lock:
                connect_future = synced.connect_future

                synced.connect_future = None
                synced.current_handler = None
                synced.close_reason = None
                synced.closed_future.set_exception(error)
                synced.state = _ClientState.DISCONNECTED
            # complete future after lock is released
            connect_future.set_exception(error)
            return

        # error is not set, so socket connection is established.
        # next step is to send CONNECT message
        try:
            logger.debug("%r connection established, sending CONNECT message", self.owner)
            # invoke callback outside of holding the lock
            if self.owner._connect_message_amender:
                amendment = self.owner._connect_message_amender()
            else:
                amendment = MessageAmendment()

            with self.owner._synced as synced:
                synced.current_connection = connection
                # check if close() was called before connection established
                if synced.state == _ClientState.DISCONNECTING:
                    logger.debug("%r close() has been called, shutting down", self.owner)
                    connection.close()
                else:
                    headers = [Header.from_string(
                        VERSION_HEADER, VERSION_STRING)]
                    # don't allow amendment to override required headers
                    existing_names = [header.name.lower() for header in headers]
                    if amendment.headers:
                        for header in amendment.headers:
                            if header.name.lower() not in existing_names:
                                headers.append(header)

                    connection.send_protocol_message(
                        headers=headers, payload=amendment.payload,
                        message_type=protocol.MessageType.CONNECT)
                    synced.state = _ClientState.WAITING_FOR_CONNECT_ACK
        except Exception as e:
            logger.debug("%r failure attempting to send CONNECT: %r", self.owner, e)
            with self.owner._synced as synced:
                synced.state = _ClientState.DISCONNECTING
                synced.current_connection = connection
                synced.close_reason = e
                connection.close()

    def on_connection_shutdown(self, reason, **kwargs):
        connect_future = None
        with self.owner._synced as synced:
            connect_future = synced.connect_future
            if reason is None:
                reason = synced.close_reason

            synced.connect_future = None
            synced.state = _ClientState.DISCONNECTED
            synced.current_handler = None
            synced.current_connection = None
            synced.close_reason = None
            if reason is None:
                synced.closed_future.set_result(None)
            else:
                synced.closed_future.set_exception(reason)

        # complete futures, and invoke callbacks, after lock is released

        # if connect_future still exists, mark that setup was a failure
        if connect_future:
            # if user called close() without a reason,
            # set a reason that the setup_future has failed
            if reason is None:
                reason = ConnectionClosedError("close() called during connection setup")
            logger.error("%r connect failed: %r", self.owner, reason)
            connect_future.set_exception(reason)
        else:
            # connect_future no longer exists, which means on_setup fired,
            # which means on_disconnect should fire now
            if reason:
                logger.info("%r disconnected, reason: %r", self.owner, reason)
            else:
                logger.info("%r disconnected", self.owner)
            self.lifecycle_handler.on_disconnect(reason)

    def on_protocol_message(self, headers, payload, message_type, flags, **kwargs):
        try:
            logger.debug("%r received %s headers=%s", self.owner, message_type.name, headers)

            # protocol enforces that CONNECT_ACK is first msg received
            if message_type == protocol.MessageType.CONNECT_ACK:
                connect_future = None
                with self.owner._synced as synced:
                    if synced.state == _ClientState.WAITING_FOR_CONNECT_ACK:
                        if (flags & protocol.MessageFlag.CONNECTION_ACCEPTED):
                            connect_future = synced.connect_future
                            synced.connect_future = None
                            synced.state = _ClientState.CONNECTED
                        else:
                            synced.state = _ClientState.DISCONNECTING
                            synced.close_reason = AccessDeniedError(
                                "Connection access denied to event stream RPC server")
                            synced.current_connection.close()
                # complete future and invoke callback after lock is released
                if connect_future:
                    logger.info("%r connected", self.owner)
                    connect_future.set_result(None)
                    self.lifecycle_handler.on_connect()
            elif message_type == protocol.MessageType.PING_RESPONSE:
                pass
            elif message_type == protocol.MessageType.PING:
                self.lifecycle_handler.on_ping(headers, payload)
            elif message_type in (protocol.MessageType.PROTOCOL_ERROR, protocol.MessageType.INTERNAL_ERROR):
                error = EventStreamError(message_type, headers, payload)
                # If callback returns True (or forgets to return a value)
                # then close connection due to error
                return_val = self.lifecycle_handler.on_error(error)
                if return_val or return_val is None:
                    self.owner.close(error)
        except Exception as e:
            logger.error("%r closing due to exception from LifecycleHandler callback: %r", self.owner, e)
            self.owner.close(e)


class Connection:
    """
    A client connection to event-stream RPC service.

    connect() must be called to open the network connection before interacting
    with the service.

    Note that close() MUST be called to end an open network connection.
    Failure to do so will result in leaked resources.

    Reconnect is possible by calling connect() again after the connection
    has finished closing/disconnecting.

    Args:
        host_name: Remote host name.

        port: Remote port.

        bootstrap: ClientBootstrap to use when initiating socket connection.

        socket_options: Optional socket options.
            If None is provided, the default options are used.

        tls_connection_options: Optional TLS connection options.
            If None is provided, then the connection will be attempted over
            plain-text.

        connect_message_amender: Optional callable that should return a
            :class:`MessageAmendment` for the
            :attr:`~awscrt.eventstream.rpc.MessageType.CONNECT` message.
            This callable will be invoked whenever a network connection is
            being established.
    """

    class _Synced:
        """
        Helper class holds all values that must not be read/written without a lock.
        """

        def __init__(self):
            self.lock = Lock()
            self.state = _ClientState.DISCONNECTED
            self.current_handler = None
            self.current_connection = None
            self.connect_future = None
            self.close_reason = None
            self.closed_future = Future()
            # closed future starts out as complete,
            # since we haven't even tried to connect yet
            self.closed_future.set_result(None)

        def __enter__(self):
            self.lock.acquire()
            return self

        def __exit__(self, type, value, tb):
            self.lock.release()

    def __init__(self,
                 *,
                 host_name: str,
                 port: int,
                 bootstrap: ClientBootstrap,
                 socket_options: Optional[SocketOptions] = None,
                 tls_connection_options: Optional[TlsConnectionOptions] = None,
                 connect_message_amender: Optional[Callable[[], MessageAmendment]] = None):

        self.host_name = host_name
        self.port = port
        self._bootstrap = bootstrap
        self._socket_options = socket_options
        self._tls_connection_options = tls_connection_options
        self._connect_message_amender = connect_message_amender

        self._synced = Connection._Synced()

    def connect(self, lifecycle_handler: LifecycleHandler) -> Future:
        """
        Asynchronously open a network connection.

        Note that close() MUST be called to end a network connection
        that is open (or in the process of connecting).
        Failure to do so will result in leaked resources.

        Args:
            lifecycle_handler: Handler for events over the course of this
                network connection. See :class:`LifecycleHandler` for more info.
                Handler methods will only be invoked if the connect attempt
                succeeds.

        Returns:
            A Future which completes when the connection succeeds or fails.
            If successful, the Future will contain None.
            Otherwise it will contain an exception explaining the reason
            for failure.
        """
        future = Future()
        future.set_running_or_notify_cancel()  # prevent cancellation
        with self._synced as synced:
            old_closed_future = synced.closed_future
            if synced.state != _ClientState.DISCONNECTED:
                raise RuntimeError("Connection already in progress")
            try:
                synced.current_handler = _ProtocolConnectionHandler(
                    self, lifecycle_handler)
                synced.connect_future = future
                synced.state = _ClientState.CONNECTING_TO_SOCKET
                # start new closed_future
                synced.closed_future = Future()
                synced.closed_future.set_running_or_notify_cancel()
                protocol.ClientConnection.connect(
                    handler=synced.current_handler,
                    host_name=self.host_name,
                    port=self.port,
                    bootstrap=self._bootstrap,
                    socket_options=self._socket_options,
                    tls_connection_options=self._tls_connection_options)
            except Exception as e:
                synced.current_handler = None
                synced.connect_future = None
                synced.closed_future = old_closed_future
                synced.state = _ClientState.DISCONNECTED
                raise e
        return future

    def close(self, reason: Optional[Exception] = None) -> Future:
        """
        Close the connection.

        Shutdown is asynchronous. This call has no effect if the connection
        is already closed or closing.

        Args:
            reason: If set, the connection will
                close with this error as the reason (unless
                it was already closing for another reason).

        Returns:
            The future which will complete
            when the shutdown process is done. The future will have an
            exception if shutdown was caused by an error, or a result
            of None if the shutdown was clean and user-initiated.
        """
        with self._synced as synced:
            if synced.state == _ClientState.DISCONNECTED:
                # do nothing, already disconnected
                pass
            elif synced.state == _ClientState.DISCONNECTING:
                # do nothing, already disconnecting for some other reason
                pass
            else:
                synced.close_reason = reason
                synced.state = _ClientState.DISCONNECTING
                # close connection if it exists.
                # if it doesn't exist yet, then it's connecting right now
                # and will get closed the moment it exists.
                if synced.current_connection:
                    synced.current_connection.close()

            return synced.closed_future

    def _send_protocol_message(self, data, message_type):
        with self._synced as synced:
            if synced.state != _ClientState.CONNECTED:
                raise ConnectionClosedError()
            return synced.current_connection.send_protocol_message(
                headers=data.headers if data else None,
                payload=data.payload if data else None,
                message_type=message_type)

    def send_ping(self, data: Optional[MessageAmendment] = None) -> Future:
        return self._send_protocol_message(data, protocol.MessageType.PING)

    def send_ping_response(self, data: Optional[MessageAmendment] = None) -> Future:
        return self._send_protocol_message(data, protocol.MessageType.PING_RESPONSE)

    def _new_stream(self, handler: protocol.ClientContinuationHandler) -> protocol.ClientContinuation:
        # public or private?
        with self._synced as synced:
            if synced.state != _ClientState.CONNECTED:
                raise ConnectionClosedError()
            return synced.current_connection.new_stream(handler)

    def __repr__(self):
        return "<%s at %#x %s:%d>" % (self.__class__.__name__, id(self), self.host_name, self.port)


class Shape:
    """
    Base class for shapes serialized by a service
    """
    @classmethod
    def _model_name(cls):
        raise NotImplementedError(cls.__name__ + " must override _model_name()")

    @classmethod
    def _from_payload(cls, payload):
        raise NotImplementedError(cls.__name__ + " must override _from_payload()")

    def _to_payload(self):
        raise NotImplementedError(self.__class__.__name__ + " must override _to_payload()")


class ErrorShape(Shape, EventStreamOperationError):
    """
    Base class for all error shapes serialized by a service
    """
    pass


class ShapeIndex:
    """
    Catalog of all shapes serialized by this service
    """

    def __init__(self, shape_types: Sequence[type]):
        self._shapes_type_by_name = {i._model_name(): i for i in shape_types}

    def find_shape_type(self, model_name: str) -> type:
        """
        Returns Shape type with given model_name, or None
        """
        return self._shapes_type_by_name.get(model_name)


class StreamResponseHandler:
    """
    Base class for all operation stream handlers.

    For operations with a streaming response (0+ messages that may arrive
    after the initial response).
    """

    def on_stream_event(self, event: Shape) -> None:
        pass

    def on_stream_error(self, error: Exception) -> bool:
        return True

    def on_stream_closed(self) -> None:
        pass


class Operation:
    """
    Base class for an operation.
    """
    @classmethod
    def _model_name(cls) -> str:
        raise NotImplementedError(cls.__name__ + " must override _model_name()")

    @classmethod
    def _request_type(cls) -> type:
        raise NotImplementedError(cls.__name__ + " must override _request_type()")

    @classmethod
    def _request_stream_type(cls) -> type:
        return None

    @classmethod
    def _response_type(cls) -> type:
        raise NotImplementedError(cls.__name__ + " must override _response_type()")

    @classmethod
    def _response_stream_type(cls) -> type:
        return None


class ClientOperation(Operation):
    """
    Base class for a client operation.

    Nearly all functions are private/protected. Child classes should
    rewrite public API to properly document the types they deal with.
    """

    def __init__(self, stream_handler: StreamResponseHandler, shape_index: ShapeIndex, connection: Connection):
        # do not instantiate directly, created by ServiceClient.new_operation()
        # all callbacks that modify state fire on the same thread,
        # so don't need locks to protect members
        self._stream_handler = stream_handler
        self._shape_index = shape_index
        self._message_count = 0
        self._closed_future = Future()
        self._closed_future.set_running_or_notify_cancel()  # prevent cancel
        self._initial_response_future = Future()
        self._initial_response_future.set_running_or_notify_cancel()  # prevent cancel
        protocol_handler = _ProtocolContinuationHandler(self)
        self._continuation = connection._new_stream(protocol_handler)

    def _activate(self, request: Shape) -> Future:
        headers = [Header.from_string(CONTENT_TYPE_HEADER,
                                      CONTENT_TYPE_APPLICATION_JSON),
                   Header.from_string(SERVICE_MODEL_TYPE_HEADER,
                                      request._model_name())]
        payload = self._json_payload_from_shape(request)
        logger.debug("%r sending request APPLICATION_MESSAGE %s %r", self, headers, payload)
        return self._continuation.activate(
            operation=self._model_name(),
            headers=headers,
            payload=payload,
            message_type=protocol.MessageType.APPLICATION_MESSAGE)

    def _send_stream_event(self, event: Shape) -> Future:
        headers = [Header.from_string(CONTENT_TYPE_HEADER,
                                      CONTENT_TYPE_APPLICATION_JSON),
                   Header.from_string(SERVICE_MODEL_TYPE_HEADER,
                                      event._model_name())]
        payload = self._json_payload_from_shape(event)
        logger.debug("%r sending event APPLICATION_MESSAGE %s %r", self, headers, payload)
        return self._continuation.send_message(
            headers=headers,
            payload=payload,
            message_type=protocol.MessageType.APPLICATION_MESSAGE)

    def _get_response(self) -> Future:
        return self._initial_response_future

    def close(self) -> Future:
        try:
            # try to send empty APPLICATION_MESSAGE with TERMINATE_STREAM flag.
            # this fails if stream is already closed, so just ignore errors.
            self._continuation.send_message(
                message_type=protocol.MessageType.APPLICATION_MESSAGE,
                flags=protocol.MessageFlag.TERMINATE_STREAM)
        except Exception:
            pass
        return self._closed_future

    def _find_header(self, headers, name, header_type=HeaderType.STRING):
        """Return header value, or None"""
        name_lower = name.lower()
        for header in headers:
            if header.name.lower() == name_lower:
                if header.type == header_type:
                    return header.value
        return None

    def _shape_from_json_payload(self, payload_bytes, shape_type):
        try:
            payload_str = payload_bytes.decode()
            payload_obj = json.loads(payload_str)
            shape = shape_type._from_payload(payload_obj)
            return shape
        except Exception as e:
            raise DeserializeError("Failed to deserialize %s" % shape_type._model_name(), e, payload_bytes)

    def _json_payload_from_shape(self, shape):
        try:
            payload_obj = shape._to_payload()
            payload_str = json.dumps(payload_obj)
            payload_bytes = payload_str.encode()
            return payload_bytes
        except Exception as e:
            raise SerializeError("Failed to serialize", shape, e)

    def _on_continuation_message(
            self,
            headers: Sequence[Header],
            payload: bytes,
            message_type: protocol.MessageType,
            flags: int,
            **kwargs):
        self._message_count += 1
        logger.debug("%r received #%d %s %s %r", self, self._message_count, message_type.name, headers, payload)
        try:
            model_name = self._find_header(headers, SERVICE_MODEL_TYPE_HEADER)
            if model_name is None:
                if flags & protocol.MessageFlag.TERMINATE_STREAM:
                    # it's ok for a TERMINATE_STREAM message to be empty
                    return
                msg = "Missing header: " + SERVICE_MODEL_TYPE_HEADER
                raise UnmappedDataError(msg, headers, payload)

            content_type = self._find_header(headers, CONTENT_TYPE_HEADER)
            if content_type is None:
                msg = "Missing header: " + CONTENT_TYPE_HEADER
                raise UnmappedDataError(msg, headers, payload)
            if content_type != CONTENT_TYPE_APPLICATION_JSON:
                msg = "Unexpected {}: '{}', expected: '{}'".format(
                    CONTENT_TYPE_HEADER, content_type, CONTENT_TYPE_APPLICATION_JSON)
                raise UnmappedDataError(msg, headers, payload)

            if message_type == protocol.MessageType.APPLICATION_MESSAGE:
                self._handle_data(model_name, payload)
                return

            # otherwise it's an APPLICATION_ERROR
            found_type = self._shape_index.find_shape_type(model_name)
            if found_type is None:
                msg = "Unknown error type: {}".format(model_name)
                raise UnmappedDataError(msg, payload)
            if not issubclass(found_type, Exception):
                msg = "Unexpected type: {} sent as APPLICATION_ERROR, expected subclass of Exception".format(model_name)
                raise UnmappedDataError(msg, payload)
            shape = self._shape_from_json_payload(payload, found_type)
            raise shape
        except Exception as e:
            self._handle_error(e, flags)

    def _handle_data(self, model_name, payload):
        """
        Pass APPLICATION_MESSAGE payload along as a 1st response,
        or subsequent stream-event. Any exceptions raised by this function
        will be passed to _handle_error().
        """
        if self._message_count == 1:
            # 1st message is "response"
            expected_type = self._response_type()
            expected_name = expected_type._model_name()
            if model_name != expected_name:
                msg = "Unexpected response type: {}, expected: {}".format(model_name, expected_name)
                raise UnmappedDataError(msg, payload)
            shape = self._shape_from_json_payload(payload, expected_type)
            self._initial_response_future.set_result(shape)
        else:
            # messages after the 1st are "stream events"
            expected_type = self._response_stream_type()
            if expected_type is None:
                msg = "Operation does not support response stream events, received type: {}".format(model_name)
                raise UnmappedDataError(msg, payload)
            expected_name = expected_type._model_name()
            if model_name != expected_name:
                msg = "Unexpected response stream event type: {}, expected: {}".format(model_name, expected_name)
                raise UnmappedDataError(msg, payload)
            shape = self._shape_from_json_payload(payload, expected_type)
            self._stream_handler.on_stream_event(shape)

    def _handle_error(self, error, message_flags):
        """
        Pass along an APPLICATION_ERROR payload, or an exception encountered while
        processing an APPLICATION_MESSAGE, as a failed 1st response
        or a stream-error.
        """
        stream_already_terminated = message_flags & protocol.MessageFlag.TERMINATE_STREAM
        try:
            if self._message_count == 1:
                # error from 1st message is "response" error.
                self._initial_response_future.set_exception(error)
                # errors on initial response must terminate the stream
                if not stream_already_terminated:
                    self.close()
            elif self._stream_handler is not None:
                # error from subsequent messages are "stream errors"
                # If this callback returns True (or forgets to return a value)
                # then close the stream
                return_val = self._stream_handler.on_stream_error(error)
                if return_val or return_val is None:
                    if not stream_already_terminated:
                        self.close()
            else:
                # this operation did not expect more than 1 message
                raise error
        except Exception:
            logger.exception("%r unhandled exception while receiving message", self)

    def _on_continuation_closed(self, **kwargs) -> None:
        logger.debug("%r closed", self)
        if not self._initial_response_future.done():
            self._initial_response_future.set_exception(StreamClosedError())

        self._closed_future.set_result(None)

        if self._stream_handler:
            try:
                self._stream_handler.on_stream_closed()
            except Exception:
                logger.exception("%r unhandled exception calling callback", self)


class _ProtocolContinuationHandler(protocol.ClientContinuationHandler):
    """Passes raw RPC stream/continuation events along to Operation"""

    def __init__(self, operation: Operation):
        self.operation = operation

    def on_continuation_message(self, *args, **kwargs):
        self.operation._on_continuation_message(*args, **kwargs)

    def on_continuation_closed(self, *args, **kwargs):
        self.operation._on_continuation_closed(*args, **kwargs)
        # break circular reference between: ClientOperation, _ProtocolContinuationHandler, ClientContinuation
        # so that garbage collector can clean them up
        self.operation = None


class Client:
    """
    Base class for a service client.

    Child class should add public API functions for each operation.
    """

    def __init__(self, connection: Connection, shape_index: ShapeIndex):
        self._connection = connection
        self._shape_index = shape_index

    def close(self, reason: Optional[Exception] = None) -> Future:
        """
        Close the connection.

        Shutdown is asynchronous. This call has no effect if the connection
        is already closed or closing.

        Args:
            reason: If set, the connection will
                close with this error as the reason (unless
                it was already closing for another reason).

        Returns:
            The future which will complete
            when the shutdown process is done. The future will have an
            exception if shutdown was caused by an error, or a result
            of None if the shutdown was clean and user-initiated.
        """
        return self._connection.close(reason=reason)

    def _new_operation(self, operation_type: type, stream_handler: StreamResponseHandler = None):
        return operation_type(stream_handler, self._shape_index, self._connection)

    @classmethod
    def _model_name(cls):
        raise NotImplementedError(cls.__name__ + " must override _model_name()")
