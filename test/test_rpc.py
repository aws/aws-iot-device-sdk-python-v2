import test.echotestrpc.model as model
import test.echotestrpc.client as client
from awsiot.eventstreamrpc import (Connection, Header, LifecycleHandler,
                                   MessageAmendment, SerializeError, StreamResponseHandler)
from awscrt.io import (ClientBootstrap, DefaultHostResolver, EventLoopGroup,
                       init_logging, LogLevel)
from datetime import datetime, timezone
import logging
import os
from queue import Queue
from sys import stderr
from threading import Event
from typing import Optional, Sequence
from unittest import skipUnless, TestCase

import awsiot.greengrasscoreipc.client

TIMEOUT = 10

#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(name)s] - %(message)s')
#init_logging(LogLevel.Trace, 'stderr')

EVENTSTREAM_ECHO_TEST = os.getenv('EVENTSTREAM_ECHO_TEST')


class ConnectionLifecycleHandler(LifecycleHandler):
    def __init__(self, on_freakout):
        self.connect_event = Event()
        self.disconnect_event = Event()
        self.disconnect_reason = None
        self.errors = Queue()
        self.pings = Queue()
        # if something happens out of order, call this
        self._freakout = on_freakout

    def on_connect(self):
        if self.disconnect_event.isSet():
            self._freakout("on_disconnect fired before on_connect()")
        if self.connect_event.isSet():
            self._freakout("on_connect fired multiple times")
        else:
            self.connect_event.set()

    def on_disconnect(self, reason: Optional[Exception]):
        if not self.connect_event.isSet():
            self._freakout("on_disconnect fired before on_connect")
        if self.disconnect_event.isSet():
            self._freakout("on_disconnect fired multiple times")
        else:
            if reason is not None and not isinstance(reason, Exception):
                self._freakout("on_disconnect reason is not an exception")
            self.disconnect_reason = reason
            self.disconnect_event.set()

    def on_error(self, error: Exception) -> bool:
        self.errors.put(error)

    def on_ping(self, headers: Sequence[Header], payload: bytes):
        self.pings.put({'headers': headers, 'payload': payload})


class StreamHandler(StreamResponseHandler):
    def __init__(self, on_freakout):
        super().__init__()
        self.events = Queue()
        self.errors = Queue()
        self.closed = Event()
        self.error_callback_return_val = True
        # set this before activating operation
        self.operation = None
        # if something happens out of order, call this
        self._freakout = on_freakout

    def on_stream_event(self, event):
        if not self.operation.get_response().done():
            self._freakout("received event before initial response")
        if self.closed.is_set():
            self._freakout("received event after close")
        self.events.put(event)

    def on_stream_error(self, error: Exception) -> bool:
        if not self.operation.get_response().done():
            self._freakout("received event before initial response")
        if self.closed.is_set():
            self._freakout("received event after close")
        if not isinstance(error, Exception):
            self._freakout("on_stream_error delivered non-error")
        self.errors.put(error)
        return self.error_callback_return_val

    def on_stream_closed(self):
        if self.closed.is_set():
            self._freakout("received closed event twice")
        self.closed.set()


def connect_amender():
    headers = [Header.from_string('client-name', 'accepted.testy_mc_testerson')]
    return MessageAmendment(headers=headers)


def bad_connect_amender():
    headers = [Header.from_string('client-name', 'rejected.testy_mc_failureson')]
    return MessageAmendment(headers=headers)


@skipUnless(EVENTSTREAM_ECHO_TEST, "Skipping until we have permanent echo server")
class RpcTest(TestCase):
    def _on_handler_freakout(self, msg):
        print(msg, file=stderr)
        if not hasattr(self, 'freakout_msg'):
            self.freakout_msg = msg

    def _assertNoHandlerFreakout(self):
        self.assertIsNone(getattr(self, 'freakout_msg', None))

    def _connect(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        self.connection = Connection(
            host_name='127.0.0.1',
            port=8033,
            bootstrap=bootstrap,
            connect_message_amender=connect_amender)
        self.lifecycle_handler = ConnectionLifecycleHandler(self._on_handler_freakout)
        connect_future = self.connection.connect(self.lifecycle_handler)
        connect_future.result(TIMEOUT)

        self.echo_client = client.EchoTestRPCClient(self.connection)

    def _bad_connect(self, bad_host=False, bad_client_name=False):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        host_name = 'badhostname' if bad_host else '127.0.0.1'
        amender = bad_connect_amender if bad_client_name else connect_amender
        self.connection = Connection(
            host_name=host_name,
            port=8033,
            bootstrap=bootstrap,
            connect_message_amender=amender)
        self.lifecycle_handler = ConnectionLifecycleHandler(self._on_handler_freakout)
        connect_future = self.connection.connect(self.lifecycle_handler)
        connect_exception = connect_future.exception(TIMEOUT)

        # connect attempt should fail
        self.assertIsNotNone(connect_exception)

        # no lifecycle events should have fired
        self.assertFalse(self.lifecycle_handler.connect_event.isSet())
        self.assertFalse(self.lifecycle_handler.disconnect_event.isSet())
        self.assertTrue(self.lifecycle_handler.errors.empty())

        self._assertNoHandlerFreakout()

    def test_connect_failed_socket(self):
        # test failure from the CONNECTING_TO_SOCKET phase
        self._bad_connect(bad_host=True)

    def test_connect_failed_connack(self):
        # test failure from the WAITING_FOR_CONNECT_ACK phse
        self._bad_connect(bad_client_name=True)

    def test_echo_message(self):
        self._connect()

        operation = self.echo_client.new_echo_message()

        request = model.EchoMessageRequest(message=model.MessageData())
        request.message.string_message = '👁👄👁'
        request.message.boolean_message = True
        # hand-picked timestamp shouldn't lose precision when serialized to
        # json as floating point. also setting timezone to UTC because
        # response timezone will always be UTC
        request.message.time_message = datetime.fromtimestamp(946684800, tz=timezone.utc)
        request.message.document_message = {
            'inty': 4,
            'floaty': 4.0,
            'listy': [1, "two", 3.0, False, True, {}, None],
            'dicty': {'a': [1, 2, 3, {'e': 9}], 'b': None},
            'stringy': "qwer",
            'booly_t': True,
            'booly_f': False,
            'nully': None,
        }
        request.message.enum_message = model.FruitEnum.BANANA
        request.message.blob_message = bytes(list(range(256)))
        request.message.string_list_message = ['one', 'two', 'three']
        request.message.key_value_pair_list = [
            model.Pair(key='key1', value='value1'),
            model.Pair(key='key1', value='value1')]

        request_flush = operation.activate(request)
        self.assertIsNone(request_flush.result(TIMEOUT))

        response = operation.get_response().result(TIMEOUT)

        self.assertIsInstance(response, model.EchoMessageResponse)
        self.assertIsInstance(response.message, model.MessageData)
        # explicit tests for each member so it's clear exactly what went wrong
        self.assertEqual(request.message.string_message, response.message.string_message)
        self.assertEqual(request.message.boolean_message, response.message.boolean_message)
        self.assertEqual(request.message.document_message, response.message.document_message)
        self.assertEqual(request.message.enum_message, response.message.enum_message)
        self.assertEqual(request.message.blob_message, response.message.blob_message)
        self.assertEqual(request.message.string_list_message, response.message.string_list_message)
        self.assertEqual(request.message.key_value_pair_list, response.message.key_value_pair_list)
        self.assertIsInstance(response.message.time_message, datetime)
        self.assertAlmostEqual(request.message.time_message.timestamp(), response.message.time_message.timestamp())

        # ok now compare a whole class
        # if this fails, it's likely due to the datetime losing precision
        # and timezone info due to datetime->timestamp->datetime conversion
        self.assertEqual(request.message, response.message)

        # must close connection
        close_future = self.connection.close()
        self.assertIsNone(close_future.exception(TIMEOUT))

        self._assertNoHandlerFreakout()

    def test_bad_activate(self):
        self._connect()

        operation = self.echo_client.new_echo_message()

        bad_request = model.EchoMessageRequest()
        bad_request.message = ".message is not supposed to be a string"

        with self.assertRaises(SerializeError):
            operation.activate(bad_request)

        # must close connection
        close_future = self.connection.close()
        self.assertIsNone(close_future.exception(TIMEOUT))

        self._assertNoHandlerFreakout()

    def test_echo_streaming_message(self):
        self._connect()

        handler = StreamHandler(self._on_handler_freakout)
        operation = self.echo_client.new_echo_stream_messages(handler)
        handler.operation = operation

        # send initial request
        flush = operation.activate(model.EchoStreamingRequest())
        flush.result(TIMEOUT)

        # send streaming request
        request_event = model.EchoStreamingMessage(key_value_pair=model.Pair(key='Kiki', value='Valerie'))
        flush = operation.send_stream_event(request_event)
        flush.result(TIMEOUT)

        # recv streaming response
        response_event = handler.events.get(timeout=TIMEOUT)
        self.assertEqual(request_event, response_event)

        # must close connection
        close_future = self.connection.close()
        self.assertIsNone(close_future.exception(TIMEOUT))
        self.assertTrue(handler.closed.is_set())

        # make sure nothing went wrong that we didn't expect to go wrong
        self.assertTrue(handler.errors.empty())
        self._assertNoHandlerFreakout()

    def test_cause_service_error(self):
        # test the CauseServiceError operation,
        # which always responds with a ServiceError
        # and then terminates the connection
        self._connect()

        operation = self.echo_client.new_cause_service_error()

        # send initial request
        operation.activate(model.CauseServiceErrorRequest())

        # get response
        response_exception = operation.get_response().exception(TIMEOUT)
        self.assertIsInstance(response_exception, model.ServiceError)

        # close connection
        close_future = self.connection.close()
        self.assertIsNone(close_future.exception(TIMEOUT))
        self._assertNoHandlerFreakout()
