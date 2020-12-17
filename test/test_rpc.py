import test.echotestrpc.model as model
import test.echotestrpc.client as client
from awsiot.eventstreamrpc import (
    AccessDeniedError,
    Connection,
    ConnectionClosedError,
    EventStreamError,
    LifecycleHandler,
    MessageAmendment,
    SerializeError,
    StreamClosedError,
    StreamResponseHandler)
from awscrt.io import (ClientBootstrap, DefaultHostResolver, EventLoopGroup,
                       init_logging, LogLevel)
from awscrt.eventstream import Header, HeaderType
from awscrt.eventstream.rpc import MessageType
from datetime import datetime, timezone
import logging
import os
from queue import Queue
from sys import stderr
from threading import Event
from time import sleep
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
        self.error_callback_return_val = True
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
        return self.error_callback_return_val

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


@skipUnless(EVENTSTREAM_ECHO_TEST, "Skipping until we have permanent echo server")
class RpcTest(TestCase):
    def _on_handler_freakout(self, msg):
        print(msg, file=stderr)
        if not hasattr(self, 'freakout_msg'):
            self.freakout_msg = msg

    def _assertNoHandlerFreakout(self):
        self.assertIsNone(getattr(self, 'freakout_msg', None))

    def setUp(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        self.connection = Connection(
            host_name='127.0.0.1',
            port=8033,
            bootstrap=bootstrap,
            connect_message_amender=connect_amender)

    def _connect(self, lifecycle_handler=None):
        if lifecycle_handler:
            self.lifecycle_handler = lifecycle_handler
        else:
            self.lifecycle_handler = ConnectionLifecycleHandler(self._on_handler_freakout)
        connect_future = self.connection.connect(self.lifecycle_handler)
        connect_future.result(TIMEOUT)
        self.echo_client = client.EchoTestRPCClient(self.connection)

    def _bad_connect(self, bad_host=False, amender=None):
        if bad_host:
            self.connection.host_name = 'badhostname'
        if amender:
            self.connection._connect_message_amender = amender
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

        return connect_exception

    def _close_connection(self):
        # helper to do normal close of healthy connection
        close_future = self.connection.close()
        close_exception = close_future.exception(TIMEOUT)
        self.assertIsNone(close_exception)
        self.assertTrue(self.lifecycle_handler.disconnect_event.wait(TIMEOUT))
        self.assertIsNone(self.lifecycle_handler.disconnect_reason)
        self.assertTrue(self.lifecycle_handler.errors.empty())
        self._assertNoHandlerFreakout()

    def test_connect_failed_socket(self):
        # test failure from the CONNECTING_TO_SOCKET phase
        self._bad_connect(bad_host=True)

    def test_connect_failed_connack(self):
        # test failure from the WAITING_FOR_CONNECT_ACK phase
        def _amender():
            headers = [Header.from_string('client-name', 'rejected.testy_mc_failureson')]
            return MessageAmendment(headers=headers)
        exception = self._bad_connect(amender=_amender)
        self.assertIsInstance(exception, AccessDeniedError)

    def test_connect_failed_amender_exception(self):
        # test failure due to connect_amender exception
        error = RuntimeError('Purposefully raising error in amender callback')

        def _amender():
            raise error
        exception = self._bad_connect(amender=_amender)
        self.assertIs(exception, error)

    def test_connect_failed_amender_bad_return(self):
        # test failure due to amender returning bad data
        def _amender():
            return 'a string is not a MessageAmendment'
        self._bad_connect(amender=_amender)

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

        self._close_connection()

    def test_bad_activate(self):
        self._connect()

        operation = self.echo_client.new_echo_message()

        bad_request = model.EchoMessageRequest()
        bad_request.message = ".message is not supposed to be a string"

        with self.assertRaises(SerializeError):
            operation.activate(bad_request)

        self._close_connection()

    def test_echo_stream_messages(self):
        self._connect()

        stream_handler = StreamHandler(self._on_handler_freakout)
        operation = self.echo_client.new_echo_stream_messages(stream_handler)
        stream_handler.operation = operation

        # send initial request
        flush = operation.activate(model.EchoStreamingRequest())
        flush.result(TIMEOUT)

        # send streaming request
        request_event = model.EchoStreamingMessage(key_value_pair=model.Pair(key='Kiki', value='Valerie'))
        flush = operation.send_stream_event(request_event)
        flush.result(TIMEOUT)

        # recv streaming response
        response_event = stream_handler.events.get(timeout=TIMEOUT)
        self.assertEqual(request_event, response_event)

        self._close_connection()
        self.assertTrue(stream_handler.closed.is_set())
        self.assertTrue(stream_handler.errors.empty())

    def test_cause_service_error(self):
        # test the CauseServiceError operation,
        # which always responds with a ServiceError
        self._connect()

        operation = self.echo_client.new_cause_service_error()

        # send initial request
        operation.activate(model.CauseServiceErrorRequest())

        # get response
        response_exception = operation.get_response().exception(TIMEOUT)
        self.assertIsInstance(response_exception, model.ServiceError)

        self._close_connection()

    def test_cause_stream_service_to_error(self):
        # test CauseStreamServiceToError operation,
        # Responds to initial request normally then throws a ServiceError on stream response
        self._connect()

        # set up operation
        stream_handler = StreamHandler(self._on_handler_freakout)
        stream_handler.error_callback_return_val = False
        op = self.echo_client.new_cause_stream_service_to_error(stream_handler)
        stream_handler.operation = op

        # send initial request, normal response should come back
        request = model.EchoStreamingRequest()
        op.activate(request)
        op.get_response().result()

        # send subsequent streaming message, streaming error should come back
        msg_to_send = model.EchoStreamingMessage(stream_message=model.MessageData())
        op.send_stream_event(msg_to_send)

        stream_error = stream_handler.errors.get(timeout=TIMEOUT)
        self.assertIsInstance(stream_error, model.ServiceError)

        self._close_connection()
        self.assertTrue(stream_handler.closed.is_set())
        self.assertTrue(stream_handler.errors.empty())

    def test_connection_error(self):
        # test that everything acts as expected if server sends
        # connection-level error
        self._connect()

        # reach deep into private inner workings of the connection to manually
        # send a bad message to the server.
        self.connection._synced.current_connection.send_protocol_message(
            headers=[Header.from_int32(':stream-id', -999)],
            message_type=MessageType.APPLICATION_MESSAGE,
        )

        # should receive PROTOCOL_ERROR in response to bad message
        error = self.lifecycle_handler.errors.get(timeout=TIMEOUT)
        self.assertIsInstance(error, EventStreamError)

        # server kills connection after PROTOCOL_ERROR
        self.assertTrue(self.lifecycle_handler.disconnect_event.wait(TIMEOUT))
        self.assertIsInstance(self.lifecycle_handler.disconnect_reason, EventStreamError)

    def test_close_with_reason(self):
        # test that, if an error is passed to connection.close(err),
        # it carries through
        self._connect()

        my_error = RuntimeError('my close reason')
        close_future = self.connection.close(my_error)
        close_reason = close_future.exception(TIMEOUT)

        self.assertIs(my_error, close_reason)
        self.assertTrue(self.lifecycle_handler.disconnect_event.wait(TIMEOUT))
        self.assertIs(my_error, self.lifecycle_handler.disconnect_reason)

    def test_reconnect(self):
        # test that a Connection can connect and disconnect multiple times
        self._connect()
        self._close_connection()

        self._connect()
        self._close_connection()

    def test_close_during_setup(self):
        # Test that it's safe to call close() while the connection is still setting up.

        # There are multiple stages to the async connect() and we'd like
        # to stress close() being called in each of these phases.
        # Hacky strategy to achieve this to, in a loop:
        # - call async connect()
        # - after some delay, call async close()
        # - with each loop, the delay gets slightly longer
        # - break out of loop loop once the delay is long enough that the
        #   connect() is completing before we ever call close()
        delay_increment_sec = 0.005
        stop_after_n_successful_connections = 2

        delay_sec = 0.0
        successful_connections = 0
        while successful_connections < stop_after_n_successful_connections:
            # not using helper _connect() call because it blocks until async connect() completes
            self.lifecycle_handler = ConnectionLifecycleHandler(self._on_handler_freakout)
            connect_future = self.connection.connect(self.lifecycle_handler)

            if delay_sec > 0.0:
                sleep(delay_sec)
            close_future = self.connection.close()

            # wait for connect and close to complete
            connect_exception = connect_future.exception(TIMEOUT)
            close_exception = close_future.exception(TIMEOUT)

            # close should have been clean
            self.assertIsNone(close_exception)

            # connect might have succeeded, or might have failed,
            # depending on the timing of this thread's close() call
            if connect_exception:
                self.assertIsInstance(connect_exception, ConnectionClosedError)
                # lifecycle handlers should NOT fire if connect setup failed
                # wait a tiny bit to be 100% sure these never fire
                self.assertFalse(self.lifecycle_handler.connect_event.wait(0.1))
                self.assertFalse(self.lifecycle_handler.disconnect_event.wait(0.1))
            else:
                self.assertTrue(self.lifecycle_handler.connect_event.wait(TIMEOUT))
                self.assertTrue(self.lifecycle_handler.disconnect_event.wait(TIMEOUT))
                successful_connections += 1

            delay_sec += delay_increment_sec
            self._assertNoHandlerFreakout()

    def test_operation_response_completes_if_connection_closed(self):
        # test that response future completes if connection is closed
        # before actual response is received.

        # this test is timing dependent, the response could theoretically
        # come on another thread before this thread can close the connection,
        # so run test in a loop till we get the timing we want
        closed_before_response = False

        # give up after a reasonably high number of tries
        # (note: first try always passes on my 2019 macbook pro, with localhost server)
        tries = 0
        max_tries = 100

        while not closed_before_response:
            self.assertLess(tries, max_tries, "Test couldn't get result it wanted after many tries")
            tries += 1

            self._connect()

            stream_handler = StreamHandler(self._on_handler_freakout)
            operation = self.echo_client.new_echo_stream_messages(stream_handler)
            stream_handler.operation = operation

            operation.activate(model.EchoStreamingRequest())
            close_future = self.connection.close()

            try:
                response = operation.get_response().result(TIMEOUT)
            except StreamClosedError:
                closed_before_response = True

            # wait for close to complete before attempting reconnect
            close_future.result(TIMEOUT)
